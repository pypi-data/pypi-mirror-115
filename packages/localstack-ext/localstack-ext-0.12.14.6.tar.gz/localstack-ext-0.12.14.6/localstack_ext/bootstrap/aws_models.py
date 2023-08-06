from localstack.utils.aws import aws_models
vQhNb=super
vQhNF=None
vQhNR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  vQhNb(LambdaLayer,self).__init__(arn)
  self.cwd=vQhNF
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.vQhNR.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,vQhNR,env=vQhNF):
  vQhNb(RDSDatabase,self).__init__(vQhNR,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,vQhNR,env=vQhNF):
  vQhNb(RDSCluster,self).__init__(vQhNR,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,vQhNR,env=vQhNF):
  vQhNb(AppSyncAPI,self).__init__(vQhNR,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,vQhNR,env=vQhNF):
  vQhNb(AmplifyApp,self).__init__(vQhNR,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,vQhNR,env=vQhNF):
  vQhNb(ElastiCacheCluster,self).__init__(vQhNR,env=env)
class TransferServer(BaseComponent):
 def __init__(self,vQhNR,env=vQhNF):
  vQhNb(TransferServer,self).__init__(vQhNR,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,vQhNR,env=vQhNF):
  vQhNb(CloudFrontDistribution,self).__init__(vQhNR,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,vQhNR,env=vQhNF):
  vQhNb(CodeCommitRepository,self).__init__(vQhNR,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
