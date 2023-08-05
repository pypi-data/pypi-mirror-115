import getpass
SnpQy=object
SnpQz=staticmethod
SnpQF=False
SnpQK=Exception
SnpQu=None
SnpQR=input
SnpQU=list
import json
import logging
import sys
from localstack.config import CONFIG_FILE_PATH,load_config_file
from localstack.constants import API_ENDPOINT
from localstack.utils.common import load_file,safe_requests,save_file,to_str
LOG=logging.getLogger(__name__)
class AuthProvider(SnpQy):
 @SnpQz
 def name():
  raise
 def get_or_create_token(self,username,password,headers):
  pass
 def get_user_for_token(self,token):
  pass
 @SnpQz
 def providers():
  return{c.name():c for c in AuthProvider.__subclasses__()}
 @SnpQz
 def get(provider,raise_error=SnpQF):
  provider_class=AuthProvider.providers().get(provider)
  if not provider_class:
   msg='Unable to find auth provider class "%s"'%provider
   LOG.warning(msg)
   if raise_error:
    raise SnpQK(msg)
   return SnpQu
  return provider_class()
class AuthProviderInternal(AuthProvider):
 @SnpQz
 def name():
  return "internal"
 def get_or_create_token(self,username,password,headers):
  data={"username":username,"password":password}
  response=safe_requests.post("%s/user/signin"%API_ENDPOINT,json.dumps(data),headers=headers)
  if response.status_code>=400:
   return
  try:
   result=json.loads(to_str(response.content or "{}"))
   return result["token"]
  except SnpQK:
   pass
 def read_credentials(self,username):
  print("Please provide your login credentials below")
  if not username:
   sys.stdout.write("Username: ")
   sys.stdout.flush()
   username=SnpQR()
  password=getpass.getpass()
  return username,password,{}
 def get_user_for_token(self,token):
  raise SnpQK("Not implemented")
def login(provider,username=SnpQu):
 auth_provider=AuthProvider.get(provider)
 if not auth_provider:
  providers=SnpQU(AuthProvider.providers().keys())
  raise SnpQK('Unknown provider "%s", should be one of %s'%(provider,providers))
 username,password,headers=auth_provider.read_credentials(username)
 print("Verifying credentials ... (this may take a few moments)")
 token=auth_provider.get_or_create_token(username,password,headers)
 if not token:
  raise SnpQK("Unable to verify login credentials - please try again")
 configs=load_config_file()
 configs["login"]={"provider":provider,"username":username,"token":token}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def logout():
 configs=json_loads(load_file(CONFIG_FILE_PATH,default="{}"))
 configs["login"]={}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def json_loads(s):
 return json.loads(to_str(s))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
