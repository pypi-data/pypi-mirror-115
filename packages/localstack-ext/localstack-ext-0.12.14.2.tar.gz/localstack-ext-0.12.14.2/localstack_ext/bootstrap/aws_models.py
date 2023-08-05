from localstack.utils.aws import aws_models
aqfwo=super
aqfwU=None
aqfwg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  aqfwo(LambdaLayer,self).__init__(arn)
  self.cwd=aqfwU
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.aqfwg.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,aqfwg,env=aqfwU):
  aqfwo(RDSDatabase,self).__init__(aqfwg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,aqfwg,env=aqfwU):
  aqfwo(RDSCluster,self).__init__(aqfwg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,aqfwg,env=aqfwU):
  aqfwo(AppSyncAPI,self).__init__(aqfwg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,aqfwg,env=aqfwU):
  aqfwo(AmplifyApp,self).__init__(aqfwg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,aqfwg,env=aqfwU):
  aqfwo(ElastiCacheCluster,self).__init__(aqfwg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,aqfwg,env=aqfwU):
  aqfwo(TransferServer,self).__init__(aqfwg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,aqfwg,env=aqfwU):
  aqfwo(CloudFrontDistribution,self).__init__(aqfwg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,aqfwg,env=aqfwU):
  aqfwo(CodeCommitRepository,self).__init__(aqfwg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
