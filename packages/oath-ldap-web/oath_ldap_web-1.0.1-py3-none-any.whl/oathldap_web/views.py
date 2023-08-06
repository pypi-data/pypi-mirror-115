# -*- coding: utf-8 -*-
"""
oathldap_web.views - method view classes
"""

import socket
import smtplib
import hashlib
import time
import email.utils

import ldap0
import ldap0.filter
import ldap0.err
from ldap0 import LDAPError
from ldap0.ldapobject import ReconnectLDAPObject
from ldap0.controls.sessiontrack import SessionTrackingControl, SESSION_TRACKING_FORMAT_OID_USERNAME
from ldap0.pw import random_string

import mailutil

from flask import current_app, request, render_template
from flask.views import MethodView

from . import RequestLogAdaptor, ExtLDAPUrl
from .forms import TokenResetForm


class Default(MethodView):
    """
    Handle requests to base URL
    """

    def __init__(self, *args, **kwargs):
        MethodView.__init__(self, *args, **kwargs)
        self.logger = RequestLogAdaptor(
            current_app.logger,
            {
                'remote_ip': request.remote_addr,
                'req_class': '.'.join((self.__class__.__module__, self.__class__.__name__)),
                'req_id': id(request),
            }
        )
        self.logger.debug(
            '%s request from %s (via %s)',
            request.method,
            request.remote_addr,
            '>'.join(request.access_route),
        )
        self.ldap_conn = None
        self.user_ldap_conn = None

    def get(self):
        """
        Simply display the entry landing page
        """
        return render_template('default.html')


class BaseApp(Default):
    """
    Request handler base class which is not used directly
    """

    def _sess_track_ctrl(self):
        """
        return LDAPv3 session tracking control representing current user
        """
        return SessionTrackingControl(
            request.remote_addr,
            request.host,
            SESSION_TRACKING_FORMAT_OID_USERNAME,
            str(id(self)),
        )

    def ldap_connect(self, authz_id=None):
        """
        Connect and bind to the LDAP directory as local system account
        """
        self.ldap_url = ExtLDAPUrl(current_app.config['LDAP_URL'])
        self.ldap_conn = ReconnectLDAPObject(
            self.ldap_url.connect_uri(),
            trace_level=current_app.config['LDAP0_TRACE_LEVEL'],
        )
        # Send SASL bind request with mechanism EXTERNAL
        self.ldap_conn.sasl_non_interactive_bind_s('EXTERNAL', authz_id=authz_id)
        # end of ldap_connect()

    def open_user_conn(self, username, password):
        """
        Search a user entry specified by :username: and check
        :password: with LDAP simple bind.
        """
        self.user_ldap_conn = None
        user = self.ldap_conn.find_unique_entry(
            self.ldap_url.dn,
            scope=self.ldap_url.scope,
            filterstr=current_app.config['FILTERSTR_ADMIN_LOGIN'].format(uid=username),
            attrlist=['1.1'],
        )
        self.user_ldap_conn = ReconnectLDAPObject(
            self.ldap_url.connect_uri(),
            trace_level=current_app.config['LDAP0_TRACE_LEVEL'],
        )
        self.user_ldap_conn.simple_bind_s(user.dn_s, password.encode('utf-8'))
        # end of BaseApp.open_user_conn()

    def search_token(self, token_serial):
        """
        Search a token entry specified by serial number
        """
        token = self.user_ldap_conn.find_unique_entry(
            self.ldap_url.dn,
            scope=self.ldap_url.scope,
            filterstr=current_app.config['FILTERSTR_TOKEN_SEARCH'].format(
                owner_attr=current_app.config['ATTR_OWNER_DN'],
                serial=token_serial,
            ),
            attrlist=[
                'createTimestamp',
                'displayName',
                'oathFailureCount',
                'oathHOTPCounter',
                'oathHOTPParams',
                'oathLastFailure',
                'oathLastLogin',
                'oathSecretTime',
                'oathTokenIdentifier',
                'oathTokenSerialNumber',
                current_app.config['ATTR_OWNER_DN'],
            ],
            req_ctrls=[self._sess_track_ctrl()],
        )
        return token.entry_s['displayName'][0], token.dn_s, token.entry_s
        # endof BaseApp.search_token()

    def do_the_work(self):
        """
        this method contains the real work and is implemented by derived classes
        """
        raise NotImplementedError(
            "method .do_the_work() not implemented in class %s.%s" % (
                self.__class__.__module__,
                self.__class__.__name__,
            )
        )


    def clean_up(self):
        """
        Clean up initialized stuff
        """
        for conn in (self.ldap_conn, self.user_ldap_conn):
            if conn:
                try:
                    self.ldap_conn.unbind_s()
                except (AttributeError, LDAPError):
                    pass
        # end of BaseApp.clean_up()

    def post(self):
        """
        Process a POST request likely resulting in some write access

        In this wrapper method only form is validated and LDAP connection
        is opened. Afterwards self.do_the_work() is called which does the
        real use-case specific work.
        """
        # Parse and validate the form input
        self.form = TokenResetForm(request.form, csrf_enabled=False)
        if not self.form.validate():
            self.logger.error(
                'Input form data not valid (%s): %s',
                self.form.__class__.__name__,
                self.form.errors,
            )
            return render_template('reset_form.html', message='Incomplete or invalid input!')
        # Make connection to LDAP server
        try:
            self.ldap_connect(authz_id=current_app.config['LDAPI_AUTHZ_ID'])
        except LDAPError as ldap_err:
            self.logger.error(
                'LDAPError connecting to %r: %s',
                self.ldap_url.connect_uri(),
                ldap_err,
            )
            return render_template('default.html', message='Internal LDAP error!')
        # Do the real work
        try:
            res = self.do_the_work()
        except Exception as err:
            self.logger.error('Unhandled exception: %s', err, exc_info=__debug__)
            res = render_template('default.html', message='Internal error!')
        self.clean_up()
        return res
        # end of BaseApp.POST()


class ResetToken(BaseApp):
    """
    Resets token to unusable state but with temporary enrollment password.

    LDAP operations are authenticated with LDAPI/SASL/EXTERNAL
    """

    def get(self):
        """
        Process the GET request mainly for displaying input form
        """
        if 'serial' not in request.args:
            message = 'Enter a serial number of token to be (re-)initialized.'
        elif 'admin' not in request.args:
            message = 'Login with your 2FA admin account.'
        return render_template(
            'reset_form.html',
            message=message,
            admin=request.args.get('admin', ''),
            serial=request.args.get('serial', ''),
        )

    def _send_pw(self, token_serial, owner_entry, enroll_pw1):
        """
        Send 2nd part of temporary password to token owner
        """

        # Open connection to SMTP relay
        #---------------------------------------------------------------
        smtp_conn = mailutil.smtp_connection(
            current_app.config['SMTP_URL'],
            local_hostname=current_app.config['SMTP_LOCALHOSTNAME'],
            ca_certs=current_app.config['SMTP_TLS_CACERTS'],
            debug_level=current_app.config['SMTP_DEBUGLEVEL'],
        )

        # Construct the message
        #---------------------------------------------------------------
        smtp_message_tmpl = open(current_app.config['EMAIL_TEMPLATE'], 'rb').read().decode('utf-8')
        to_addr = owner_entry['mail'][0]
        default_headers = (
            ('From', current_app.config['SMTP_FROM']),
            ('Date', email.utils.formatdate(time.time(), True)),
        )
        owner_data = {
            'serial': token_serial,
            'admin': self.form.admin.data,
            'enrollpw1': enroll_pw1,
            'remote_ip': request.remote_addr,
            'fromaddr': current_app.config['SMTP_FROM'],
        }
        smtp_message = smtp_message_tmpl % owner_data
        smtp_subject = current_app.config['EMAIL_SUBJECT'] % owner_data

        # Send the message
        #---------------------------------------------------------------
        smtp_conn.send_simple_message(
            current_app.config['SMTP_FROM'],
            [to_addr],
            'utf-8',
            default_headers+(
                ('Subject', smtp_subject),
                ('To', to_addr),
            ),
            smtp_message,
        )
        smtp_conn.quit()
        self.logger.info('Sent reset password to %r.', to_addr)
        # end of _send_pw()

    def search_accounts(self, token_dn):
        """
        Search all accounts using the token
        """
        ldap_result = self.user_ldap_conn.search_s(
            self.ldap_url.dn,
            ldap0.SCOPE_SUBTREE,
            filterstr='(&(objectClass=oathUser)(oathToken={dn}))'.format(
                dn=ldap0.filter.escape_str(token_dn),
            ),
            attrlist=['uid', 'description']
        )
        if not ldap_result:
            return None
        return [
            (
                res.entry_s['uid'][0],
                res.entry_s.get('description', [''])[0],
            )
            for res in ldap_result
        ]

    def read_owner(self, owner_dn):
        """
        Read a token owner entry
        """
        ldap_result = self.user_ldap_conn.read_s(
            owner_dn,
            filterstr=current_app.config['FILTERSTR_OWNER_READ'],
            attrlist=[
                'displayName',
                'mail',
                'telePhoneNumber',
                'mobile',
                'l',
            ],
        )
        if ldap_result:
            result = ldap_result.entry_s
        else:
            raise ldap0.NO_SUCH_OBJECT(
                'No result with %r' % (current_app.config['FILTERSTR_OWNER_READ'],)
            )
        return result
        # end of read_owner()

    def update_token(self, token_dn, token_entry, token_password):
        """
        Resets token to unusable state by
        - overwriting 'oathSecret'
        - removing 'oathLastLogin'
        - removing 'oathHOTPCounter'
        - removing failure attributes 'oathFailureCount' and 'oathLastFailure'
        - setting temporary enrollment password in 'userPassword'
        - resetting 'oathSecretTime' to current time
        """
        session_tracking_ctrl = self._sess_track_ctrl()
        token_mods = [
            # We don't fully trust enrollment client
            # => set shared secret time to current time here
            (
                ldap0.MOD_REPLACE,
                b'oathSecretTime',
                [time.strftime('%Y%m%d%H%M%SZ', time.gmtime(time.time())).encode('ascii')],
            ),
        ]
        for del_attr in (
                'oathHOTPCounter',
                'oathLastLogin',
                'oathFailureCount',
                'oathLastFailure',
            ):
            if del_attr in token_entry:
                token_mods.append(
                    (ldap0.MOD_DELETE, del_attr.encode('ascii'), None)
                )
        # Reset the token entry
        self.user_ldap_conn.modify_s(
            token_dn,
            token_mods,
            req_ctrls=[session_tracking_ctrl],
        )
        # Try to remove shared secret separately because with
        # strict access control we don't know whether it's set or not
        try:
            self.user_ldap_conn.modify_s(
                token_dn,
                [(ldap0.MOD_DELETE, b'oathSecret', None)],
                req_ctrls=[session_tracking_ctrl],
            )
        except ldap0.NO_SUCH_ATTRIBUTE:
            # We can happily ignore this case
            pass
        # Set the new userPassword with Modify Password ext.op.
        # for server-side hashing
        self.ldap_conn.passwd_s(
            token_dn,
            None, token_password,
            req_ctrls=[session_tracking_ctrl],
        )
        # end of ResetToken.update_token()

    def do_the_work(self):
        """
        Actually do the work herein
        """
        # Check the user login and open user connection
        self.logger.debug('Will try login as user %r', self.form.admin.data)
        try:
            self.open_user_conn(self.form.admin.data, self.form.password.data)
        except LDAPError as ldap_err:
            self.logger.error(
                'Error opening user connection to %r as user %r: %s',
                self.ldap_url.connect_uri(),
                self.form.admin.data,
                ldap_err,
            )
            return render_template('reset_form.html', message='Admin login failed!')
        token_serial = self.form.serial.data
        try:
            token_displayname, token_dn, token_entry = self.search_token(
                token_serial
            )
            owner_dn = token_entry[current_app.config['ATTR_OWNER_DN']][0]
            owner_entry = self.read_owner(owner_dn)
            accounts = self.search_accounts(token_dn)
            confirm_hash = hashlib.sha256(
                ''.join((
                    token_serial,
                    owner_dn,
                    str(sorted(accounts or [])),
                )).encode('utf-8')
            ).hexdigest()
            if self.form.confirm.data != confirm_hash:
                return render_template(
                    'reset_form.html',
                    message='Please confirm token reset. Examine this information carefully!',
                    admin=self.form.admin.data,
                    serial=self.form.serial.data,
                    token=token_displayname,
                    owner=owner_entry['displayName'][0],
                    email=owner_entry['mail'][0],
                    accounts=accounts,
                    confirm=confirm_hash,
                )
            enroll_pw1 = random_string(
                alphabet=current_app.config['PWD_TMP_CHARS'],
                length=current_app.config['PWD_LENGTH']-current_app.config['PWD_ADMIN_LEN'],
                )
            enroll_pw2 = random_string(
                alphabet=current_app.config['PWD_TMP_CHARS'],
                length=current_app.config['PWD_ADMIN_LEN'],
            )
            enroll_pw = enroll_pw1 + enroll_pw2
            self.update_token(token_dn, token_entry, enroll_pw)
        except ldap0.err.NoUniqueEntry as ldap_err:
            self.logger.warning('LDAPError: %s', ldap_err)
            return render_template('reset_form.html', message='Serial no. not found!')
        except LDAPError as ldap_err:
            self.logger.error('LDAPError: %s', ldap_err, exc_info=__debug__)
            return render_template('reset_form.html', message='Internal LDAP error!')
        except Exception as err:
            self.logger.error('Unhandled exception: %s', err, exc_info=__debug__)
            return render_template('reset_form.html', message='Internal error!')
        # try to send 2nd enrollment password part to token owner
        try:
            self._send_pw(self.form.serial.data, owner_entry, enroll_pw1)
        except (socket.error, socket.gaierror, smtplib.SMTPException) as mail_error:
            self.logger.error(
                'Error sending e-mail to owner of device %s: %s',
                self.form.serial.data,
                mail_error,
                exc_info=__debug__
            )
            return render_template('reset_form.html', message='Error sending e-mail via SMTP!')
        self.logger.info('Finished resetting token %r.', token_dn)
        return render_template(
            'reset_action.html',
            message='Token was reset',
            serial=token_serial,
            token=token_entry['displayName'][0],
            owner=owner_entry['displayName'][0],
            email=owner_entry['mail'][0],
            enrollpw2=enroll_pw2,
        )
        # end of ResetToken.do_the_work()
