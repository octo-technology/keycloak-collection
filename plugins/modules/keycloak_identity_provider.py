#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2017, Philippe Gauthier INSPQ <philippe.gauthier@inspq.qc.ca>
#
# This file is not part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
author: "Philippe Gauthier (philippe.gauthier@inspq.qc.ca"
module: keycloak_identity_provider
short_description: Configure an identity provider in Keycloak
description:
  - This module creates, removes or update Keycloak identity provider.
version_added: "1.1"
options:
  url:
    description:
    - The url of the Keycloak server.
    default: http://localhost:8080/auth
    required: true    
  username:
    description:
    - The username to logon to the master realm.
    required: true
  password:
    description:
    - The password for the user to logon the master realm.
    required: true
  realm:
    description:
    - The name of the realm in which is the identity provider.
    required: true
  alias:
    description:
    - The alias of the identity provider.
    required: true
  displayName:
    description:
    - The display name of the realm.
    required: false
  providerId:
    description:
    - Type of identity provider.
    required: false
  enabled:
    description:
    - enabled.
    required: false
    default: true
  updateProfileFirstLoginMode:
    description:
    - update Profile First Login Mode.
    required: false
  trustEmail:
    description: 
    - trust Email.
    required: false
  storeToken:
    description:
    - store Token.
    required: false
    default: true
  addReadTokenRoleOnCreate:
    description:
    - add Read Token Role On Create.
    required: false
  authenticateByDefault:
    description:
    - authenticate By Default.
    required: false
  firstBrokerLoginFlowAlias:
    description:
    - first Broker Login Flow Alias.
    required: false
  postBrokerLoginFlowAlias:
    description:
    - post Broker Login Flow Alias.
    required: false
  config:
    description:
    - Detailed configuration of the identity provider. 
    required: false
  mappers:
    description:
    - List of mappers for the Identity provider.
    required: false
  state:
    description:
    - Control if the realm exists.
    choices: [ "present", "absent" ]
    default: present
    required: false
  force:
    choices: [ "yes", "no" ]
    default: "no"
    description:
    - If yes, allows to remove realm and recreate it.
    required: false
notes:
  - module does not modify identity provider alias.
'''

EXAMPLES = '''
    - name: Create IdP1 fully configured with idp user attribute mapper and a role mapper
      keycloak_identity_provider:
        realm: "master"
        url: "http://localhost:8080"
        username: "admin"
        password: "password"  
        alias: "IdP1"
        displayName: "My super dooper IdP"
        providerId: "oidc"
        config:
          openIdConfigurationUrl: https://my.idp.com/auth
          clientId: ClientIdMyIdpGaveMe
          clientSecret: ClientSecretMyIdpGaveMe
          disableUserInfo: False
          defaultScope: "openid email profile"
          guiOrder: 1
        mappers:
          - name: ClaimMapper
            identityProviderMapper: oidc-user-attribute-idp-mapper
            config:
              claim: claim1
              user.attribute: attr1
          - name: MyRoleMapper
            identityProviderMapper: oidc-role-idp-mapper
            config:
              claim: claimName
              claim.value: valueThatGiveRole
              role: roleName
        state: present

    - name: Re-create the Idp1 without mappers. The existing Idp will be deleted.
      keycloak_identity_provider:
        realm: "master"
        url: "http://localhost:8080"
        username: "admin"
        password: "password"  
        alias: "IdP1"
        displayName: "My super dooper IdP"
        providerId: "oidc"
        config:
          openIdConfigurationUrl: https://my.idp.com/auth
          clientId: ClientIdMyIdpGaveMe
          clientSecret: ClientSecretMyIdpGaveMe
          disableUserInfo: False
          defaultScope: "openid email profile"
          guiOrder: 2
        state: present
        force: yes

    - name: Remove a the Idp IdP1.
      keycloak_identity_provider:
        alias: IdP1
        state: absent
'''

RETURN = '''
ansible_facts:
  description: JSON representation for the identity provider.
  returned: on success
  type: dict
stderr:
  description: Error message if it is the case
  returned: on error
  type: str
rc:
  description: return code, 0 if success, 1 otherwise.
  returned: always
  type: bool
changed:
  description: Return True if the operation changed the identity provider on the keycloak server, false otherwise.
  returned: always
  type: bool
'''
import requests
import json
import urllib
import copy
from ansible_collections.inspq.keycloak.plugins.module_utils.keycloak_utils import *
    
def addIdPEndpoints(idPConfiguration, url):
    '''
fonction :      addIdPEndpoints
description:    Cette fonction permet d'intéroger le endpoint openid-configuration d'un fournisseur
                d'identité afin d'en extraire les différents endpoints à mettre dans l'objet
                config de keycloak.
paramètres:
    idPConfiguration:
    type: dict
    description: Dictionnaire contenant ls structure config à compléter.
    url:
    type: str
    description: URL de la configuration OpenID connect à intérroger
    '''
#    url = None
#    if 'openIdConfigurationUrl' in idPConfiguration.keys():
#        url = idPConfiguration["openIdConfigurationUrl"]
#        del idPConfiguration["openIdConfigurationUrl"]
    if url is not None:
        try:
            openidConfigRequest = requests.get(url, verify=False)
            openIdConfig = openidConfigRequest.json()
            if 'userinfo_endpoint' in openIdConfig.keys():
                idPConfiguration["userInfoUrl"] = openIdConfig["userinfo_endpoint"]
            if 'token_endpoint' in openIdConfig.keys():
                idPConfiguration["tokenUrl"] = openIdConfig["token_endpoint"]
            if 'jwks_uri' in openIdConfig.keys():
                idPConfiguration["jwksUrl"] = openIdConfig["jwks_uri"]
            if 'issuer' in openIdConfig.keys():
                idPConfiguration["issuer"] = openIdConfig["issuer"]
            if 'authorization_endpoint' in openIdConfig.keys():
                idPConfiguration["authorizationUrl"] = openIdConfig["authorization_endpoint"]
            if 'end_session_endpoint' in openIdConfig.keys():
                idPConfiguration["logoutUrl"] = openIdConfig["end_session_endpoint"]        
        except Exception as e:
            raise e

def deleteAllMappers(url, bearerHeader):
    changed = False
    try:
        # Obtenir la liste des mappers existant
        getMappersRequest = requests.get(url + '/mappers', headers={'Authorization' : bearerHeader})
        mappers = getMappersRequest.json()
        for mapper in mappers:
            requests.delete(url + '/mappers/' + mapper['id'], headers={'Authorization' : bearerHeader})
    except requests.exceptions.RequestException as ValueError:
        return False
    except Exception as e:
        raise e
     
    return changed

def createOrUpdateMappers(url, headers, alias, idPMappers):
    changed = False
    create = False
   
    try:
        # Obtenir la liste des mappers existant
        getMappersRequest = requests.get(url + '/mappers', headers=headers)
        try:
            mappers = getMappersRequest.json()
        except ValueError: # Il n'y a pas de mapper de défini pour cet IdP
            mappers = []
            create = True
        for idPMapper in idPMappers:
            mapperFound = False
            mapperId = ""
            for mapper in mappers:
                if mapper['name'] == idPMapper['name']:
                    mapperFound = True
                    break
            # If mapper already exist and is different
            if mapperFound and not isDictEquals(idPMapper,mapper):
                # update the existing mapper
                for key in idPMapper.keys():
                    mapper[key] = idPMapper[key]
                    data=json.dumps(mapper)
                    response = requests.put(url + '/mappers/' + mapper["id"], headers=headers, data=data)
                changed = True
            # If the mapper does not already exist
            if not mapperFound:
                # Complete the mapper settings with defaults
                if 'identityProviderMapper' not in idPMapper.keys(): # si le type de mapper a été fourni
                    idPMapper['identityProviderMapper'] = 'oidc-user-attribute-idp-mapper'                
                idPMapper['identityProviderAlias'] = alias
 
                # Create it
                data=json.dumps(idPMapper)
                response = requests.post(url + '/mappers', headers=headers, data=data)
                changed = True
                
    except Exception as e :
        raise e
    return changed
                    

def main():
    module = AnsibleModule(
        argument_spec = dict(
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
            realm=dict(type='str', required=True),
            alias=dict(type='str', required=True),
            displayName=dict(type='str'),
            providerId=dict(type='str'),
            enabled = dict(type='bool', default=True),
            updateProfileFirstLoginMode=dict(type='str'),
            trustEmail=dict(type='bool'),
            storeToken = dict(type='bool', default=True),
            addReadTokenRoleOnCreate = dict(type='bool'),
            authenticateByDefault = dict(type='bool'),
            firstBrokerLoginFlowAlias = dict(type='str'),
            postBrokerLoginFlowAlias = dict(type='str'),
            config = dict(type='dict'),
            mappers = dict(type='list'),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    
    
    params = module.params.copy()
    
    result = idp(params, module)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
    
def idp(params, module = None):
    url = params['url']
    username = params['username']
    password = params['password']
    realm = params['realm']
    state = params['state']
    force = module.boolean(module.params['force']) if module is not None else params['force']
    rc = 0
    result = dict()
    changed = False
    idPExists = False
    # Créer un représentation du realm recu en paramètres
    newIdPRepresentation = {}
    if 'alias' in params and params['alias'] is not None and len(params['alias']) > 0:
        newIdPRepresentation["alias"] = params['alias'].decode("utf-8")
        queryParams = {'alias': params['alias'].decode("utf-8")}
    else:
        #if 'config' in params and 'clientId' in params['config']:
        #    queryParams = {'clientId': params['config']['clientId'].decode("utf-8")}
        #else:
        result = dict(
            stderr   = 'Alias must be provided',
            rc       = 1,
            changed  = changed
            )
        return result
    if 'displayName' in params and params['displayName'] is not None:
        newIdPRepresentation["displayName"] = params['displayName'].decode("utf-8")
    if 'providerId' in params and params['providerId'] is not None:
        newIdPRepresentation["providerId"] = params['providerId'].decode("utf-8")
    if 'enabled' in params:
        newIdPRepresentation["enabled"] = module.boolean(params['enabled']) if module is not None else params['enabled']
    if 'updateProfileFirstLoginMode' in params and params['updateProfileFirstLoginMode'] is not None:
        newIdPRepresentation["updateProfileFirstLoginMode"] = params['updateProfileFirstLoginMode'].decode("utf-8")
    if 'trustEmail' in params and params["trustEmail"] is not None:
        newIdPRepresentation["trustEmail"] = module.boolean(params['trustEmail']) if module is not None else params['trustEmail']
    if 'storeToken' in params and params["storeToken"] is not None:
        newIdPRepresentation["storeToken"] = module.boolean(params['storeToken']) if module is not None else params['storeToken']
    if 'addReadTokenRoleOnCreate' in params and params["addReadTokenRoleOnCreate"] is not None:
        newIdPRepresentation["addReadTokenRoleOnCreate"] = module.boolean(params['addReadTokenRoleOnCreate']) if module is not None else params['addReadTokenRoleOnCreate']
    if 'authenticateByDefault' in params and params["authenticateByDefault"] is not None:
        newIdPRepresentation["authenticateByDefault"] = module.boolean(params['authenticateByDefault']) if module is not None else params['authenticateByDefault']
    if 'firstBrokerLoginFlowAlias' in params and params['firstBrokerLoginFlowAlias'] is not None:
        newIdPRepresentation["firstBrokerLoginFlowAlias"] = params['firstBrokerLoginFlowAlias'].decode("utf-8")
    if 'postBrokerLoginFlowAlias' in params and params['postBrokerLoginFlowAlias'] is not None:
        newIdPRepresentation["postBrokerLoginFlowAlias"] = params['postBrokerLoginFlowAlias'].decode("utf-8")

    newIdPConfig = None
    if 'config' in params and params['config'] is not None:
        #newIdPConfig = params['config']
        newIdPConfig = {}  
        for param, value in params["config"].iteritems():
            if param != 'openIdConfigurationUrl':
                newIdPConfig[param] = value
  
    if 'providerId' in newIdPRepresentation and newIdPRepresentation["providerId"] == 'google' and 'userIp' in params["config"]:
        newIdPConfig["userIp"] = params["config"]["userIp"]
    newIdPMappers = params['mappers'] if 'mappers' in params else None
    
    idPSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/identity-provider/instances/"
    
    #print str(newIdPRepresentation)

    try:
        #accessToken = login(url, username, password)
        #bearerHeader = "bearer " + accessToken
        headers = loginAndSetHeaders(url, username, password)
    except Exception as e:
        result = dict(
            stderr   = 'login: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
    try:
        if newIdPConfig is not None:
            if 'openIdConfigurationUrl' in params['config']:
                addIdPEndpoints(newIdPConfig, params["config"]['openIdConfigurationUrl'])
        
            newIdPRepresentation["config"] = newIdPConfig
    except Exception as e:
        result = dict(
            stderr   = 'addIdPEndpoints: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result

    try: 
        # Vérifier si le IdP existe sur le serveur Keycloak
        getResponse = requests.get(idPSvcBaseUrl, headers=headers)
        listIdPs = getResponse.json()
        
        for idP in listIdPs:
            if ('alias' in queryParams and idP['alias'] == queryParams['alias']) or ('clientId' in queryParams and idP['config']['clientId'] == queryParams['clientId']):
                idPExists = True
                # Obtenir le IdP exitant
                idPRepresentation = idP
                break
                
        #print str(queryParams)
        #print str(getResponse.json())
    except Exception as e:
        result = dict(
            stderr   = 'first realm get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    
   
    if not idPExists: # Le IdP n'existe pas
        # Creer le IdP
        if not 'alias' in newIdPRepresentation:
            result = dict(
                stderr   = 'No Alias provided while creating a new Identity Provider or updating a non existing identity provider',
                rc       = 1,
                changed  = changed
                )
            return result
        idPSvcUrl = idPSvcBaseUrl + newIdPRepresentation['alias']
        if (state == 'present'): # Si le status est présent
            try:
                # Stocker le IdP dans un body prêt a être posté
                data=json.dumps(newIdPRepresentation)
                # Créer le IdP
                postResponse = requests.post(idPSvcBaseUrl, headers=headers, data=data)
                # S'il y a des mappers de définis pour l'IdP
                if newIdPMappers is not None and len(newIdPMappers) > 0:
                    createOrUpdateMappers(idPSvcUrl, headers, newIdPRepresentation["alias"], newIdPMappers)
                # Obtenir le nouvel IdP créé
                getResponse = requests.get(idPSvcUrl, headers=headers)
                changed = True
                idPRepresentation = getResponse.json()
                
                getResponse = requests.get(idPSvcUrl + "/mappers", headers=headers)
                try:
                    mappersRepresentation = getResponse.json()
                except ValueError:
                    mappersRepresentation = {}
                
                fact = dict(
                    idp = idPRepresentation,
                    mappers = mappersRepresentation)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException as e:
                fact = dict(
                    idp = newIdPRepresentation)
                result = dict(
                    ansible_facts= fact,
                    stderr   = 'post idp: ' + newIdPRepresentation["alias"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError as e:
                fact = dict(
                    idp = newIdPRepresentation)
                result = dict(
                    ansible_facts = fact,
                    stderr   = 'post idp: ' + newIdPRepresentation["alias"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        else: # Sinon, le status est absent
            result = dict(
                stdout   = newIdPRepresentation["alias"] + ' absent',
                rc       = 0,
                changed  = changed
            )
                
    else:  # Le realm existe déjà
        alias = idPRepresentation['alias']
        idPSvcUrl = idPSvcBaseUrl + alias
        try:
            if (state == 'present'): # si le status est présent
                
                if force: # Si l'option force est sélectionné
                    # Supprimer les mappings existants
                    deleteAllMappers(idPSvcUrl, bearerHeader)
                    # Supprimer le IdP existant
                    deleteResponse = requests.delete(idPSvcUrl, headers=headers)
                    changed = True
                    # Stocker le IdP dans un body prêt a être posté
                    data=json.dumps(newIdPRepresentation)
                    # Créer le nouveau IdP
                    postResponse = requests.post(idPSvcBaseUrl, headers=headers, data=data)
                else: # Si l'option force n'est pas sélectionné
                    # Comparer les realms
                    if not isDictEquals(newIdPRepresentation, idPRepresentation, ["clientSecret", "openIdConfigurationUrl", "mappers"]) or ("config" in newIdPRepresentation and "clientSecret" in newIdPRepresentation["config"] and newIdPRepresentation["config"]["clientSecret"] is not None): # Si le nouveau IdP n'introduit pas de modification au IdP existant
                    #if not isDictEquals(newIdPRepresentation, idPRepresentation): # Si le nouveau IdP n'introduit pas de modification au IdP existant
                        # S'il y a un changement
                        # Mettre a jour la representation existante
                        updatedIdP = copy.deepcopy(idPRepresentation)
                        updatedIdP.update(newIdPRepresentation)
                        if "config" in newIdPRepresentation and newIdPRepresentation["config"] is not None:
                            updatedConfig = idPRepresentation["config"]
                            updatedConfig.update(newIdPRepresentation["config"])
                            updatedIdP["config"] = updatedConfig
                        #with open("/tmp/keycloak_idp.log","a") as f:
                        #    f.write(str(updatedIdP))
                        #f.close()
                        # Stocker le IdP dans un body prêt a être posté
                        data=json.dumps(updatedIdP)
                        # Mettre à jour le IdP sur le serveur Keycloak
                        updateResponse = requests.put(idPSvcUrl, headers=headers, data=data)
                        changed = True
                if newIdPMappers is not None and len(newIdPMappers) > 0:
                    if createOrUpdateMappers(idPSvcUrl, headers, alias, newIdPMappers):
                        changed = True
        
                # Obtenir sa représentation JSON sur le serveur Keycloak                        
                getResponse = requests.get(idPSvcUrl, headers=headers)
                idPRepresentation = getResponse.json()
                
                getResponse = requests.get(idPSvcUrl + "/mappers", headers=headers)
                try:
                    mappersRepresentation = getResponse.json()
                except ValueError:
                    mappersRepresentation = {}
                
                fact = dict(
                    idp = idPRepresentation,
                    mappers = mappersRepresentation)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            else: # Le status est absent
                # Supprimer le IdP
                deleteResponse = requests.delete(idPSvcUrl, headers=headers)
                changed = True
                result = dict(
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException as e:
            result = dict(
                stderr   = 'put or delete idp: ' + str(newIdPRepresentation) + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError as e:
            result = dict(
                stderr   = 'put or delete idp: ' + str(newIdPRepresentation) + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    
    return result
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
