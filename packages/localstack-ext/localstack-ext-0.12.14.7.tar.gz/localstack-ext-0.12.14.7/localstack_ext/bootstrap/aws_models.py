from localstack.utils.aws import aws_models
LpAdl=super
LpAdM=None
LpAdS=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  LpAdl(LambdaLayer,self).__init__(arn)
  self.cwd=LpAdM
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.LpAdS.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,LpAdS,env=LpAdM):
  LpAdl(RDSDatabase,self).__init__(LpAdS,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,LpAdS,env=LpAdM):
  LpAdl(RDSCluster,self).__init__(LpAdS,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,LpAdS,env=LpAdM):
  LpAdl(AppSyncAPI,self).__init__(LpAdS,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,LpAdS,env=LpAdM):
  LpAdl(AmplifyApp,self).__init__(LpAdS,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,LpAdS,env=LpAdM):
  LpAdl(ElastiCacheCluster,self).__init__(LpAdS,env=env)
class TransferServer(BaseComponent):
 def __init__(self,LpAdS,env=LpAdM):
  LpAdl(TransferServer,self).__init__(LpAdS,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,LpAdS,env=LpAdM):
  LpAdl(CloudFrontDistribution,self).__init__(LpAdS,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,LpAdS,env=LpAdM):
  LpAdl(CodeCommitRepository,self).__init__(LpAdS,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
