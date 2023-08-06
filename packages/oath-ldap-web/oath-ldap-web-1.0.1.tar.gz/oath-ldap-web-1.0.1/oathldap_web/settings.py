# -*- coding: utf-8 -*-
"""
Configuration module for oathenroll
"""

import secrets

# URL path prefix used when generating URLs in e-mails
# handy for reverse proxy setups
APPLICATION_ROOT = '/oath'

# generate a 64-bytes random secret
APP_SECRET = secrets.token_bytes(64)

# default log level
LOG_LEVEL = 'info'

# logger name
LOG_NAME = 'oathldap_web'

# path of logging config file
LOG_CONFIG = None

# number of proxy levels
# see https://werkzeug.palletsprojects.com/en/1.0.x/middleware/proxy_fix/
PROXY_LEVEL = 0

# Trace level for ldap0 logs
LDAP0_TRACE_LEVEL = 0

# LDAP-URL describing the connection parameters and bind information
LDAP_URL = 'ldapi:///ou=ae-dir??sub??trace=0,x-saslmech=EXTERNAL'

# SASL authz-ID to be sent along with SASL/EXTERNAL bind
LDAPI_AUTHZ_ID = None

# Filter string template for finding an active admin entry during login
# Notes:
# - must require initialized 2FA user account with filter part (&(objectClass=oathUser)(oathHOTPToken=*))
# - authorization is enforced via filter part (|(memberOf=cn=otp-zone-admins,cn=otp,ou=ae-dir)(memberOf=cn=ae-admins,cn=ae,ou=ae-dir))
FILTERSTR_ADMIN_LOGIN = (
    '(&(objectClass=aeUser)(uid={uid})'
#    '(objectClass=oathUser)(oathHOTPToken=*)'  # enforces 2FA user account
    ')'
)

ATTR_OWNER_DN = 'owner'

# Filter string template for reading a particular active owner entry
# (require initialized 2FA user account herein)
FILTERSTR_OWNER_READ = '(&(objectClass=inetOrgPerson)(aeStatus=0))'

# Filter string template for finding an active token entry
FILTERSTR_TOKEN_SEARCH = '(&(objectClass=device)({owner_attr}=*)(objectClass=oathToken)(serialNumber=yubikey-{serial})(aeHwSerialNumber={serial})(oathTokenSerialNumber={serial}))'

# Name of directory containing all the template files
TEMPLATES_DIRNAME = '/etc/oath-ldap/oathenroll/templates/'

# Format string for displaying date and time
TIME_DISPLAY_FORMAT = '%Y-%m-%d %H:%M:%S'

# Length of generated temporary passwords
PWD_LENGTH = 12

# Number of chars of generated temporary passwords to be displayed to 2FA admin
PWD_ADMIN_LEN = 6

# Characters used for the temporary passwords
PWD_TMP_CHARS = 'abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ23456789'

# Filename of template for sending e-mail message to user
EMAIL_SUBJECT = 'Your temporary enrollment password for Yubikey #%(serial)s'
EMAIL_TEMPLATE = TEMPLATES_DIRNAME+'reset.txt'

# SMTP server used as smart host (SMTP relay)
SMTP_URL = 'smtp://mail.example.com/?STARTTLS'

# Debug level for SMTP messages sent to stderr
SMTP_DEBUGLEVEL = 0

# Hostname to be sent in EHLO request,
# set to None for automatically using the local hostname
SMTP_LOCALHOSTNAME = 'ae-dir-suse-p1.vnet1.local'

# Path name of file containing CA certificates used to validate TLS server certs
SMTP_TLS_CACERTS = '/opt/ae-dir/etc/my-ae-dir-testca-2017-06.pem'

# From address in sent e-mail
SMTP_FROM = 'oath-ldap-admins@example.com'
