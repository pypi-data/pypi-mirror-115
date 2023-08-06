from localstack.utils.aws import aws_models
eEuHo=super
eEuHp=None
eEuHB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  eEuHo(LambdaLayer,self).__init__(arn)
  self.cwd=eEuHp
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.eEuHB.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,eEuHB,env=eEuHp):
  eEuHo(RDSDatabase,self).__init__(eEuHB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,eEuHB,env=eEuHp):
  eEuHo(RDSCluster,self).__init__(eEuHB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,eEuHB,env=eEuHp):
  eEuHo(AppSyncAPI,self).__init__(eEuHB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,eEuHB,env=eEuHp):
  eEuHo(AmplifyApp,self).__init__(eEuHB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,eEuHB,env=eEuHp):
  eEuHo(ElastiCacheCluster,self).__init__(eEuHB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,eEuHB,env=eEuHp):
  eEuHo(TransferServer,self).__init__(eEuHB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,eEuHB,env=eEuHp):
  eEuHo(CloudFrontDistribution,self).__init__(eEuHB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,eEuHB,env=eEuHp):
  eEuHo(CodeCommitRepository,self).__init__(eEuHB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
