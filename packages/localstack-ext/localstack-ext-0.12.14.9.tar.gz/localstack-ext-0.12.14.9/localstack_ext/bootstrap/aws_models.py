from localstack.utils.aws import aws_models
bpmhP=super
bpmhU=None
bpmhY=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  bpmhP(LambdaLayer,self).__init__(arn)
  self.cwd=bpmhU
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.bpmhY.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,bpmhY,env=bpmhU):
  bpmhP(RDSDatabase,self).__init__(bpmhY,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,bpmhY,env=bpmhU):
  bpmhP(RDSCluster,self).__init__(bpmhY,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,bpmhY,env=bpmhU):
  bpmhP(AppSyncAPI,self).__init__(bpmhY,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,bpmhY,env=bpmhU):
  bpmhP(AmplifyApp,self).__init__(bpmhY,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,bpmhY,env=bpmhU):
  bpmhP(ElastiCacheCluster,self).__init__(bpmhY,env=env)
class TransferServer(BaseComponent):
 def __init__(self,bpmhY,env=bpmhU):
  bpmhP(TransferServer,self).__init__(bpmhY,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,bpmhY,env=bpmhU):
  bpmhP(CloudFrontDistribution,self).__init__(bpmhY,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,bpmhY,env=bpmhU):
  bpmhP(CodeCommitRepository,self).__init__(bpmhY,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
