#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, INSPQ <philippe.gauthier@inspq.qc.ca>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: keycloak_realm
short_description: Configure a realm in Keycloak
description:
  - This module creates, removes or update Keycloak realms.
version_added: "2.9"
options:
    realm:
        description:
            - The name of the realm.
        default: master
        type: str
    displayName:
        description:
            - The display name of the realm.
        required: true
        aliases: ['name']
        type: str
    displayNameHtml:
        description:
            - The name to use within the HTML page of the realm.
        required: false
        aliases: ['namehtml']
        type: str
    loginTheme:
        description:
            - Theme to use at logon for this realm.
        required: false
        type: str
    adminTheme:
        description:
            - Theme to use for this realm's admin console.
        required: false
        type: str
    emailTheme:
        description:
            - Theme to use for this realm's emails.
        required: false
        type: str
    accountTheme:
        description:
            - Theme to use for this realm's accounts.
        required: false
        type: str
    internationalizationEnabled:
        description:
            - Is internationalization enabled for this realm?
        required: false
        type: bool
    supportedLocales:
        description:
            - List of supported languages for the realm.
        required: false
        type: list
    defaultLocale:
        description:
            - If multiple locales are supported, which one will be used as default language.
        required: false
        type: str
    accessCodeLifespan:
        description:
            - access code lifespan.
        default: 60
        type: int
    accessCodeLifespanLogin:
        description:
            - access code lifespan login.
        default: 1800
        type: int
    accessCodeLifespanUserAction:
        description:
            - access code lifespan user action.
        default: 300
        type: int
    accessTokenLifespan:
        description:
            - Access token lifespan.
        default: 300
        type: int
    accessTokenLifespanForImplicitFlow:
        description:
            - Access token lifespan for implicit flow.
        default: 900
        type: int
    notBefore:
        description:
            - Not Before.
        type: int
    revokeRefreshToken:
        description:
            - Revoke Refresh Token.
        type: bool
    ssoSessionMaxLifespan:
        description:
            - Sso Session Max Lifespan.
        default: 36000
        type: int
    offlineSessionIdleTimeout:
        description:
            - Offline Session Idle Timeout.
        default: 2592000
        type: int
    ssoSessionIdleTimeout:
        description:
            - SSO session idle timeout.
        default: 1800
        type: int
    enabled:
        description:
            - Enabled.
        default: True
        type: bool
    sslRequired:
        description:
            - SSL Required.
        default: external
        type: str
    registrationAllowed:
        description:
            - Registration Allowed.
        default: False
        type: bool
    registrationEmailAsUsername:
        description:
            - Registration Email As Username.
        default: False
        type: bool
    rememberMe:
        description:
            - Remember me.
        default: False
        type: bool
    verifyEmail:
        description:
            - Verify Email.
        default: False
        type: bool
    loginWithEmailAllowed:
        description:
            - Login With Email Allowed.
        default: True
        type: bool
    duplicateEmailsAllowed:
        description:
            - Duplicate Emails Allowed.
        type: bool
        required: false
    resetPasswordAllowed:
        description:
            - Reset Password Allowed.
        default: False
        type: bool
    editUsernameAllowed:
        description:
            - Edit Username Allowed.
        default: False
        type: bool
    bruteForceProtected:
        description:
            - Brute Force Protected.
        default: False
        type: bool
    permanentLockout:
        description:
            - Permanent Lockout.
        default: False
        type: bool
    maxFailureWaitSeconds:
        description:
            - Max Failure Wait Seconds.
        default: 900
        type: int
    minimumQuickLoginWaitSeconds:
        description:
            - Minimum Quick Login Wait Seconds.
        default: 60
        type: int
    waitIncrementSeconds:
        description:
            - Wait Increment Seconds.
        default: 60
        type: int
    quickLoginCheckMilliSeconds:
        description:
            - Quick Login Check MilliSeconds.
        default: 1000
        type: int
    maxDeltaTimeSeconds:
        description:
            - Max Delta Time Seconds.
        default: 43200
        type: int
    failureFactor:
        description:
            - Failure Factor.
        default: 30
        type: int
    defaultRoles:
        description:
            - Default roles.
        default: [ "offline_access", "uma_authorization" ]
        type: list
    requiredCredentials:
        description:
            - Required Credentials.
        default: [ "password" ]
        type: list
    passwordPolicy:
        description:
            - Password Policy.
        default: hashIterations(20000)
        required: false
        type: str
    otpPolicyType:
        description:
            - Otp Policy Type.
        default: totp
        type: str
    otpPolicyAlgorithm:
        description:
            - Otp Policy Algorithm.
        default: HmacSHA1
        type: str
    otpPolicyInitialCounter:
        description:
            - Otp Policy Initial Counter.
        default: 0
        type: int
    otpPolicyDigits:
        description:
            - Otp Policy Digits.
        default: 6
        type: int
    otpPolicyLookAheadWindow:
        description:
            - Otp Policy Look Ahead Window.
        default: 1
        type: int
    otpPolicyPeriod:
        description:
            - Otp Policy Period.
        default: 30
        type: int
    smtpServer:
        description:
        - SMTP Server.
        default: {}
        required: false
        type: dict
        suboptions:
            replyToDisplayName:
                description:
                    - Name to display in sent email reply to field.
                type: str
            starttls:
                description:
                    - If true, enable Start TLS.
                    - Default is false if not defined.
                type: str
                choices:
                    - 'true'
                    - 'false'
                default: 'false'
            auth:
                description:
                    - Is authentication enabled on the SMTP server.
                    - Default is false if not defined.
                type: str
                choices:
                    - 'true'
                    - 'false'
                default: 'false'
            port:
                description:
                    - SMTP server port.
                type: str
                default: '25'
            host:
                description:
                    - SMTP server host name or ip address.
                type: str
            replyTo:
                description:
                    - Reply to address to put in sent email.
                type: str
            from:
                description:
                    - From address to put in sent email.
                type: str
            fromDisplayName:
                description:
                    - Name to put in from field for sent email.
                type: str
            envelopeFrom:
                description:
                    - Address to put in envelopeFrom field for sent email.
                type: str
            ssl:
                description:
                    - If true, SSL will be used to connect to SMTP server
                type: str
                choices:
                    - 'true'
                    - 'false'
                default: 'false'
            user:
                description:
                    - User name to authenticate on SMTP server if authentication is enabled.
                type: str
            password:
                description:
                    - Password of the user to authenticate on SMTP server.
                type: str
    eventsConfig:
        description:
            - Event configuration for the realm.
        required: false
        type: dict
        suboptions:
            eventsEnabled:
                description:
                    - If true, enable event loggin for the realm.
                type: bool
            enabledEventTypes:
                description:
                    - Types of event to log.
                type: list
                choices:
                    - SEND_RESET_PASSWORD
                    - UPDATE_TOTP
                    - REMOVE_TOTP
                    - REVOKE_GRANT
                    - LOGIN_ERROR
                    - CLIENT_LOGIN
                    - RESET_PASSWORD_ERROR
                    - IMPERSONATE_ERROR
                    - CODE_TO_TOKEN_ERROR
                    - CUSTOM_REQUIRED_ACTION
                    - UPDATE_PROFILE_ERROR
                    - IMPERSONATE
                    - LOGIN
                    - UPDATE_PASSWORD_ERROR
                    - REGISTER
                    - LOGOUT
                    - CLIENT_REGISTER
                    - UPDATE_PASSWORD
                    - FEDERATED_IDENTITY_LINK_ERROR
                    - CLIENT_DELETE
                    - IDENTITY_PROVIDER_FIRST_LOGIN
                    - VERIFY_EMAIL
                    - CLIENT_DELETE_ERROR
                    - CLIENT_LOGIN_ERROR
                    - REMOVE_FEDERATED_IDENTITY_ERROR
                    - EXECUTE_ACTIONS
                    - SEND_IDENTITY_PROVIDER_LINK_ERROR
                    - SEND_VERIFY_EMAIL
                    - EXECUTE_ACTIONS_ERROR
                    - REMOVE_FEDERATED_IDENTITY
                    - IDENTITY_PROVIDER_POST_LOGIN
                    - UPDATE_EMAIL
                    - REGISTER_ERROR
                    - REVOKE_GRANT_ERROR
                    - LOGOUT_ERROR
                    - UPDATE_EMAIL_ERROR
                    - CLIENT_UPDATE_ERROR
                    - UPDATE_PROFILE
                    - FEDERATED_IDENTITY_LINK
                    - CLIENT_REGISTER_ERROR
                    - SEND_VERIFY_EMAIL_ERROR
                    - SEND_IDENTITY_PROVIDER_LINK
                    - RESET_PASSWORD
                    - REMOVE_TOTP_ERROR
                    - VERIFY_EMAIL_ERROR
                    - SEND_RESET_PASSWORD_ERROR
                    - CLIENT_UPDATE
                    - IDENTITY_PROVIDER_POST_LOGIN_ERROR
                    - CUSTOM_REQUIRED_ACTION_ERROR
                    - UPDATE_TOTP_ERROR
                    - CODE_TO_TOKEN
                    - IDENTITY_PROVIDER_FIRST_LOGIN_ERROR
            eventsListeners:
                description:
                    - List of event listeners to log.
                type: list
            adminEventsEnabled:
                description:
                    - If true, administration events will be logged.
                type: bool
            adminEventsDetailsEnabled:
                description:
                    - If true, detail of administration event will be added to the logs.
                type: bool
            eventsExpiration:
                description:
                    - backup time of logs in keycloak.
                required: false
                type: int
    browserFlow:
        description:
            - Browser Flow.
        default: browser
        type: str
    registrationFlow:
        description:
            - Registration Flow.
        default: registration
        required: false
        type: str
    directGrantFlow:
        description:
            - Direct Grant Flow.
        default: direct grant
        type: str
    resetCredentialsFlow:
        description:
            - Reset Credentials Flow.
        default: reset credentials
        type: str
    clientAuthenticationFlow:
        description:
            - Client Authentication Flow.
        default: clients
        type: str
    attributes:
        description:
            - Attributes.
        required: false
        type: dict
    browserSecurityHeaders:
        description:
            - Browser Security Headers.
        required: false
        type: dict
    state:
        choices: [ "present", "absent" ]
        default: present
        description:
            - Control if the realm exists.
        type: str
    force:
        type: bool
        default: false
        description:
            - If true, allows to remove realm and recreate it.
extends_documentation_fragment:
    - keycloak
notes:
  - module does not modify realm name.
author:
    - Philippe Gauthier (@elfelip)
'''

EXAMPLES = '''
    - name: Create a realm
      keycloak_realm:
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
        realm: realm1
        name: "realm1"
        namehtml: "The first Realm"
        smtpServer:
          replyToDisplayName: root
          starttls: ""
          auth: ""
          port: "25"
          host: "localhost"
          replyTo: "root@localhost"
          from: "root@localhost"
          fromDisplayName: "local"
          envelopeFrom: "root@localhost"
          ssl: ""
        eventsConfig:
          eventsEnabled: true
          eventsListeners :
            - jboss-logging
            - sx5-event-listener
          adminEventsEnabled: true
          adminEventsDetailsEnabled: false
        state : present

    - name: Re-create the realm realm1
      keycloak_realm:
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
        realm: realm1
        name: "realm1"
        namehtml: "The first Realm"
        state : present
        force: yes

    - name: Remove a the realm realm1.
      keycloak_realm:
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
        name: realm1
        state: absent
'''

RETURN = '''
realm:
  description: JSON representation for the REALM.
  returned: on success
  type: dict
eventsConfig:
  description: Events configuration for the realm.
  returned: on success
  type: dict
msg:
  description: Error message if it is the case
  returned: on error
  type: str
changed:
  description: Return True if the operation changed the REALM on the keycloak server, false otherwise.
  returned: always
  type: bool
'''

from ansible_collections.inspq.keycloak.plugins.module_utils.keycloak import KeycloakAPI, camel, \
    keycloak_argument_spec, get_token, KeycloakError, isDictEquals, remove_arguments_with_value_none
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = keycloak_argument_spec()
    smtp_spec = {
        "replyToDisplayName": {
            "type": "str"
        },
        "starttls": {
            "type": "str",
            "choices": [
                "true",
                "false"
            ],
            "default": "false"
        },
        "auth": {
            "type": "str",
            "choices": [
                "true",
                "false"
            ],
            "default": "false"
        },
        "port": {
            "type": "str",
            "default": "25"
        },
        "host": {
            "type": "str"
        },
        "replyTo": {
            "type": "str"
        },
        "from": {
            "type": "str"
        },
        "fromDisplayName": {
            "type": "str"
        },
        "envelopeFrom": {
            "type": "str"
        },
        "ssl": {
            "type": "str",
            "choices": [
                "true",
                "false"
            ],
            "default": "false"
        },
        "user": {
            "type": "str"
        },
        "password": {
            "type": "str",
            "no_log": True
        }
    }
    eventconfig_spec = {
        "eventsEnabled": {
            "type": "bool"
        },
        "eventsListeners": {
            "type": "list"
        },
        "adminEventsEnabled": {
            "type": "bool"
        },
        "adminEventsDetailsEnabled": {
            "type": "bool"
        },
        "eventsExpiration": {
            "type": "int"
        },
        "enabledEventTypes": {
            "type": "list",
            "choices": [
                "SEND_RESET_PASSWORD",
                "UPDATE_TOTP",
                "REMOVE_TOTP",
                "REVOKE_GRANT",
                "LOGIN_ERROR",
                "CLIENT_LOGIN",
                "RESET_PASSWORD_ERROR",
                "IMPERSONATE_ERROR",
                "CODE_TO_TOKEN_ERROR",
                "CUSTOM_REQUIRED_ACTION",
                "UPDATE_PROFILE_ERROR",
                "IMPERSONATE",
                "LOGIN",
                "UPDATE_PASSWORD_ERROR",
                "REGISTER",
                "LOGOUT",
                "CLIENT_REGISTER",
                "UPDATE_PASSWORD",
                "FEDERATED_IDENTITY_LINK_ERROR",
                "CLIENT_DELETE",
                "IDENTITY_PROVIDER_FIRST_LOGIN",
                "VERIFY_EMAIL",
                "CLIENT_DELETE_ERROR",
                "CLIENT_LOGIN_ERROR",
                "REMOVE_FEDERATED_IDENTITY_ERROR",
                "EXECUTE_ACTIONS",
                "SEND_IDENTITY_PROVIDER_LINK_ERROR",
                "SEND_VERIFY_EMAIL",
                "EXECUTE_ACTIONS_ERROR",
                "REMOVE_FEDERATED_IDENTITY",
                "IDENTITY_PROVIDER_POST_LOGIN",
                "UPDATE_EMAIL",
                "REGISTER_ERROR",
                "REVOKE_GRANT_ERROR",
                "LOGOUT_ERROR",
                "UPDATE_EMAIL_ERROR",
                "CLIENT_UPDATE_ERROR",
                "UPDATE_PROFILE",
                "FEDERATED_IDENTITY_LINK",
                "CLIENT_REGISTER_ERROR",
                "SEND_VERIFY_EMAIL_ERROR",
                "SEND_IDENTITY_PROVIDER_LINK",
                "RESET_PASSWORD",
                "REMOVE_TOTP_ERROR",
                "VERIFY_EMAIL_ERROR",
                "SEND_RESET_PASSWORD_ERROR",
                "CLIENT_UPDATE",
                "IDENTITY_PROVIDER_POST_LOGIN_ERROR",
                "CUSTOM_REQUIRED_ACTION_ERROR",
                "UPDATE_TOTP_ERROR",
                "CODE_TO_TOKEN",
                "IDENTITY_PROVIDER_FIRST_LOGIN_ERROR"
            ]
        }
    }
    meta_args = dict(
        realm=dict(type='str', default='master'),
        displayName=dict(type='str', required=True, aliases=['name']),
        displayNameHtml=dict(type='str', default="", aliases=['namehtml']),
        loginTheme=dict(type="str"),
        adminTheme=dict(type="str"),
        emailTheme=dict(type="str"),
        accountTheme=dict(type="str"),
        internationalizationEnabled=dict(type="bool"),
        supportedLocales=dict(type="list"),
        defaultLocale=dict(type="str"),
        accessCodeLifespan=dict(type='int', default=60),
        accessCodeLifespanLogin=dict(type='int', default=1800),
        accessCodeLifespanUserAction=dict(type='int', default=300),
        notBefore=dict(type='int', default=0),
        revokeRefreshToken=dict(type='bool', default=False),
        accessTokenLifespan=dict(type='int', default=300),
        accessTokenLifespanForImplicitFlow=dict(type='int', default=900),
        ssoSessionIdleTimeout=dict(type='int', default=1800),
        ssoSessionMaxLifespan=dict(type='int', default=36000),
        offlineSessionIdleTimeout=dict(type='int', default=2592000),
        enabled=dict(type='bool', default=True),
        sslRequired=dict(type='str', default="external"),
        registrationAllowed=dict(type='bool', default=False),
        registrationEmailAsUsername=dict(type='bool', default=False),
        rememberMe=dict(type='bool', default=False),
        verifyEmail=dict(type='bool', default=False),
        loginWithEmailAllowed=dict(type='bool', default=True),
        duplicateEmailsAllowed=dict(type='bool', default=False),
        resetPasswordAllowed=dict(type='bool', default=False),
        editUsernameAllowed=dict(type='bool', default=False),
        bruteForceProtected=dict(type='bool', default=False),
        permanentLockout=dict(type='bool', default=False),
        maxFailureWaitSeconds=dict(type='int', default=900),
        minimumQuickLoginWaitSeconds=dict(type='int', default=60),
        waitIncrementSeconds=dict(type='int', default=60),
        quickLoginCheckMilliSeconds=dict(type='int', default=1000),
        maxDeltaTimeSeconds=dict(type='int', default=43200),
        failureFactor=dict(type='int', default=30),
        defaultRoles=dict(type='list', default=["offline_access", "uma_authorization"]),
        requiredCredentials=dict(type='list', default=["password"]),
        passwordPolicy=dict(type='str', default="hashIterations(20000)"),
        otpPolicyType=dict(type='str', default="totp"),
        otpPolicyAlgorithm=dict(type='str', default="HmacSHA1"),
        otpPolicyInitialCounter=dict(type='int', default=0),
        otpPolicyDigits=dict(type='int', default=6),
        otpPolicyLookAheadWindow=dict(type='int', default=1),
        otpPolicyPeriod=dict(type='int', default=30),
        smtpServer=dict(type='dict', default={}, options=smtp_spec),
        eventsConfig=dict(type='dict', options=eventconfig_spec),
        browserFlow=dict(type='str', default="browser"),
        registrationFlow=dict(type='str', default="registration"),
        directGrantFlow=dict(type='str', default="direct grant"),
        resetCredentialsFlow=dict(type='str', default="reset credentials"),
        clientAuthenticationFlow=dict(type='str', default="clients"),
        state=dict(choices=["absent", "present"], default='present'),
        force=dict(type='bool', default=False),
        attributes=dict(type='dict', default=None),
        browserSecurityHeaders=dict(type='dict', default=None)
    )

    argument_spec.update(meta_args)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = dict(changed=False, msg='', realm={}, eventsConfig={})

    # Obtain access token, initialize API
    try:
        connection_header = get_token(
            base_url=module.params.get('auth_keycloak_url'),
            validate_certs=module.params.get('validate_certs'),
            auth_realm=module.params.get('auth_realm'),
            client_id=module.params.get('auth_client_id'),
            auth_username=module.params.get('auth_username'),
            auth_password=module.params.get('auth_password'),
            client_secret=module.params.get('auth_client_secret'),
        )
    except KeycloakError as e:
        module.fail_json(msg=str(e))

    kc = KeycloakAPI(module, connection_header)

    defaultAttributes = dict(
        _browser_header=dict(
            contentSecurityPolicy=dict(type='unicode', default="frame-src 'self'"),
            xContentTypeOptions=dict(type='unicode', default="nosniff"),
            xFrameOptions=dict(type='unicode', default="SAMEORIGIN"),
            xRobotsTag=dict(type='unicode', default="none"),
            xXSSProtection=dict(type='unicode', default="1; mode=block")
        ),
        actionTokenGeneratedByAdminLifespan=dict(type='int', default=43200),
        actionTokenGeneratedByUserLifespan=dict(type='int', default=300),
        displayName=dict(type='unicode', default=module.params.get('name')),
        displayNameHtml=dict(type='unicode', default=module.params.get('namehtml')),
    )
    defaultBrowserSecurityHeaders = dict(
        contentSecurityPolicy=dict(type='unicode', default="frame-src 'self'"),
        xContentTypeOptions=dict(type='unicode', default="nosniff"),
        xFrameOptions=dict(type='unicode', default="SAMEORIGIN"),
        xRobotsTag=dict(type='unicode', default="none"),
        xXSSProtection=dict(type='unicode', default="1; mode=block")
    )

    state = module.params.get('state')
    force = module.params.get('force')

    # Create a realm representation form module parameters
    newRealmRepresentation = {}
    newRealmRepresentation["id"] = module.params.get('realm')
    newRealmRepresentation["realm"] = module.params.get('realm')
    newRealmRepresentation["displayName"] = module.params.get('displayName')
    newRealmRepresentation["displayNameHtml"] = module.params.get('displayNameHtml')
    if module.params.get("loginTheme") is not None:
        newRealmRepresentation["loginTheme"] = module.params.get("loginTheme")
    if module.params.get("adminTheme") is not None:
        newRealmRepresentation["adminTheme"] = module.params.get("adminTheme")
    if module.params.get("emailTheme") is not None:
        newRealmRepresentation["emailTheme"] = module.params.get("emailTheme")
    if module.params.get("accountTheme") is not None:
        newRealmRepresentation["accountTheme"] = module.params.get("accountTheme")
    newRealmRepresentation["accessCodeLifespan"] = module.params.get('accessCodeLifespan')
    newRealmRepresentation["accessCodeLifespanLogin"] = module.params.get('accessCodeLifespanLogin')
    newRealmRepresentation["accessCodeLifespanUserAction"] = module.params.get('accessCodeLifespanUserAction')
    newRealmRepresentation["notBefore"] = module.params.get('notBefore')
    newRealmRepresentation["revokeRefreshToken"] = module.params.get('revokeRefreshToken')
    newRealmRepresentation["accessTokenLifespan"] = module.params.get('accessTokenLifespan')
    newRealmRepresentation["accessTokenLifespanForImplicitFlow"] = module.params.get('accessTokenLifespanForImplicitFlow')
    newRealmRepresentation["ssoSessionIdleTimeout"] = module.params.get('ssoSessionIdleTimeout')
    newRealmRepresentation["ssoSessionMaxLifespan"] = module.params.get('ssoSessionMaxLifespan')
    newRealmRepresentation["offlineSessionIdleTimeout"] = module.params.get('offlineSessionIdleTimeout')
    newRealmRepresentation["enabled"] = module.params.get('enabled')
    newRealmRepresentation["sslRequired"] = module.params.get('sslRequired')
    newRealmRepresentation["registrationAllowed"] = module.params.get('registrationAllowed')
    newRealmRepresentation["registrationEmailAsUsername"] = module.params.get('registrationEmailAsUsername')
    newRealmRepresentation["rememberMe"] = module.params.get('rememberMe')
    newRealmRepresentation["verifyEmail"] = module.params.get('verifyEmail')
    newRealmRepresentation["loginWithEmailAllowed"] = module.params.get('loginWithEmailAllowed')
    newRealmRepresentation["duplicateEmailsAllowed"] = module.params.get('duplicateEmailsAllowed')
    newRealmRepresentation["resetPasswordAllowed"] = module.params.get('resetPasswordAllowed')
    newRealmRepresentation["editUsernameAllowed"] = module.params.get('editUsernameAllowed')
    newRealmRepresentation["bruteForceProtected"] = module.params.get('bruteForceProtected')
    newRealmRepresentation["permanentLockout"] = module.params.get('permanentLockout')
    newRealmRepresentation["maxFailureWaitSeconds"] = module.params.get('maxFailureWaitSeconds')
    newRealmRepresentation["minimumQuickLoginWaitSeconds"] = module.params.get('minimumQuickLoginWaitSeconds')
    newRealmRepresentation["waitIncrementSeconds"] = module.params.get('waitIncrementSeconds')
    newRealmRepresentation["quickLoginCheckMilliSeconds"] = module.params.get('quickLoginCheckMilliSeconds')
    newRealmRepresentation["maxDeltaTimeSeconds"] = module.params.get('maxDeltaTimeSeconds')
    newRealmRepresentation["failureFactor"] = module.params.get('failureFactor')
    newRealmRepresentation["defaultRoles"] = module.params.get('defaultRoles')
    newRealmRepresentation["requiredCredentials"] = module.params.get('requiredCredentials')
    newRealmRepresentation["passwordPolicy"] = module.params.get('passwordPolicy')
    newRealmRepresentation["otpPolicyType"] = module.params.get('otpPolicyType')
    newRealmRepresentation["otpPolicyAlgorithm"] = module.params.get('otpPolicyAlgorithm')
    newRealmRepresentation["otpPolicyInitialCounter"] = module.params.get('otpPolicyInitialCounter')
    newRealmRepresentation["otpPolicyDigits"] = module.params.get('otpPolicyDigits')
    newRealmRepresentation["otpPolicyLookAheadWindow"] = module.params.get('otpPolicyLookAheadWindow')
    newRealmRepresentation["otpPolicyPeriod"] = module.params.get('otpPolicyPeriod')
    newRealmRepresentation["smtpServer"] = module.params.get('smtpServer')
    remove_arguments_with_value_none(newRealmRepresentation["smtpServer"])
    if module.params.get("supportedLocales") is not None:
        if module.params.get("internationalizationEnabled") is not None:
            newRealmRepresentation["internationalizationEnabled"] = module.params.get("internationalizationEnabled")
        else:
            newRealmRepresentation["internationalizationEnabled"] = True
        newRealmRepresentation["supportedLocales"] = module.params.get("supportedLocales")
        if module.params.get("defaultLocale") is not None:
            newRealmRepresentation["defaultLocale"] = module.params.get("defaultLocale")
    else:
        newRealmRepresentation["internationalizationEnabled"] = False
    newRealmRepresentation["browserFlow"] = module.params.get('browserFlow')
    newRealmRepresentation["registrationFlow"] = module.params.get('registrationFlow')
    newRealmRepresentation["directGrantFlow"] = module.params.get('directGrantFlow')
    newRealmRepresentation["resetCredentialsFlow"] = module.params.get('resetCredentialsFlow')
    newRealmRepresentation["clientAuthenticationFlow"] = module.params.get('clientAuthenticationFlow')
    if module.params.get("eventsExpiration") is not None:
        newRealmRepresentation["eventsExpiration"] = module.params.get('eventsExpiration')
    # Read Events configuration for the Realm
    newEventsConfig = module.params.get("eventsConfig")
    remove_arguments_with_value_none(newEventsConfig)
    if module.params.get("browserSecurityHeaders") is not None:
        newRealmRepresentation["browserSecurityHeaders"] = module.params.get("browserSecurityHeaders")

    changed = False
    # Find realm on Keycloak server
    realmRepresentation = kc.search_realm(realm=newRealmRepresentation["realm"])
    if realmRepresentation == {}:  # Realm does not exist
        if (state == 'present'):  # If desired state is present
            # Create the realm
            result["realm"] = kc.create_realm(newRealmRepresentation=newRealmRepresentation)
            if newEventsConfig is not None:
                eventsConfig = kc.update_realm_events_config(realm=newRealmRepresentation["realm"], newEventsConfig=newEventsConfig)
                result["eventsConfig"] = eventsConfig
            changed = True
        else:  # if desired state is absent
            result['msg'] = 'Realm %s is absent' % (newRealmRepresentation["realm"])

    else:  # Realm already exists
        if (state == 'present'):  # If desired state is present
            if force:  # If force option is true
                # Delete the existing realm
                kc.delete_realm(newRealmRepresentation["realm"])
                # Create realm
                realmRepresentation = kc.create_realm(newRealmRepresentation=newRealmRepresentation)
                changed = True
            else:  # If force option is false
                # Compare realms
                if not isDictEquals(newRealmRepresentation, realmRepresentation):  # If new realm introduces changes
                    # Update REALM
                    realmRepresentation = kc.update_realm(newRealmRepresentation=newRealmRepresentation)
                    changed = True
                else:
                    realmRepresentation = kc.get_realm(realm=newRealmRepresentation["realm"])
            if newEventsConfig is not None:  # If there is event configuration
                # Get the existing events config
                eventsConfig = kc.get_realm_events_config(realm=newRealmRepresentation["realm"])
                if not isDictEquals(newEventsConfig, eventsConfig):  # If realm needs changed
                    # Update event config
                    eventsConfig = kc.update_realm_events_config(realm=newRealmRepresentation["realm"], newEventsConfig=newEventsConfig)
                result["eventsConfig"] = eventsConfig
            result["realm"] = realmRepresentation
        else:  # If desired state is absent
            # Delete Realm
            kc.delete_realm(newRealmRepresentation["realm"])
            changed = True
            result["msg"] = 'Realm %s deleted' % (newRealmRepresentation["realm"])
    result["changed"] = changed
    module.exit_json(**result)


if __name__ == '__main__':
    main()
