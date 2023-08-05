from localstack.utils.aws import aws_models
WnRYH=super
WnRYm=None
WnRYd=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  WnRYH(LambdaLayer,self).__init__(arn)
  self.cwd=WnRYm
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.WnRYd.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,WnRYd,env=WnRYm):
  WnRYH(RDSDatabase,self).__init__(WnRYd,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,WnRYd,env=WnRYm):
  WnRYH(RDSCluster,self).__init__(WnRYd,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,WnRYd,env=WnRYm):
  WnRYH(AppSyncAPI,self).__init__(WnRYd,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,WnRYd,env=WnRYm):
  WnRYH(AmplifyApp,self).__init__(WnRYd,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,WnRYd,env=WnRYm):
  WnRYH(ElastiCacheCluster,self).__init__(WnRYd,env=env)
class TransferServer(BaseComponent):
 def __init__(self,WnRYd,env=WnRYm):
  WnRYH(TransferServer,self).__init__(WnRYd,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,WnRYd,env=WnRYm):
  WnRYH(CloudFrontDistribution,self).__init__(WnRYd,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,WnRYd,env=WnRYm):
  WnRYH(CodeCommitRepository,self).__init__(WnRYd,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
