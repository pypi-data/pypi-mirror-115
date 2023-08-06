from localstack.utils.aws import aws_models
CbRWv=super
CbRWn=None
CbRWM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  CbRWv(LambdaLayer,self).__init__(arn)
  self.cwd=CbRWn
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.CbRWM.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,CbRWM,env=CbRWn):
  CbRWv(RDSDatabase,self).__init__(CbRWM,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,CbRWM,env=CbRWn):
  CbRWv(RDSCluster,self).__init__(CbRWM,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,CbRWM,env=CbRWn):
  CbRWv(AppSyncAPI,self).__init__(CbRWM,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,CbRWM,env=CbRWn):
  CbRWv(AmplifyApp,self).__init__(CbRWM,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,CbRWM,env=CbRWn):
  CbRWv(ElastiCacheCluster,self).__init__(CbRWM,env=env)
class TransferServer(BaseComponent):
 def __init__(self,CbRWM,env=CbRWn):
  CbRWv(TransferServer,self).__init__(CbRWM,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,CbRWM,env=CbRWn):
  CbRWv(CloudFrontDistribution,self).__init__(CbRWM,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,CbRWM,env=CbRWn):
  CbRWv(CodeCommitRepository,self).__init__(CbRWM,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
