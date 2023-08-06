from localstack.utils.aws import aws_models
aFMjE=super
aFMjb=None
aFMjq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  aFMjE(LambdaLayer,self).__init__(arn)
  self.cwd=aFMjb
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.aFMjq.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,aFMjq,env=aFMjb):
  aFMjE(RDSDatabase,self).__init__(aFMjq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,aFMjq,env=aFMjb):
  aFMjE(RDSCluster,self).__init__(aFMjq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,aFMjq,env=aFMjb):
  aFMjE(AppSyncAPI,self).__init__(aFMjq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,aFMjq,env=aFMjb):
  aFMjE(AmplifyApp,self).__init__(aFMjq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,aFMjq,env=aFMjb):
  aFMjE(ElastiCacheCluster,self).__init__(aFMjq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,aFMjq,env=aFMjb):
  aFMjE(TransferServer,self).__init__(aFMjq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,aFMjq,env=aFMjb):
  aFMjE(CloudFrontDistribution,self).__init__(aFMjq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,aFMjq,env=aFMjb):
  aFMjE(CodeCommitRepository,self).__init__(aFMjq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
