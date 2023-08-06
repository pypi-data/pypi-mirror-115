from localstack.utils.aws import aws_models
XAxJV=super
XAxJg=None
XAxJC=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  XAxJV(LambdaLayer,self).__init__(arn)
  self.cwd=XAxJg
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.XAxJC.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,XAxJC,env=XAxJg):
  XAxJV(RDSDatabase,self).__init__(XAxJC,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,XAxJC,env=XAxJg):
  XAxJV(RDSCluster,self).__init__(XAxJC,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,XAxJC,env=XAxJg):
  XAxJV(AppSyncAPI,self).__init__(XAxJC,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,XAxJC,env=XAxJg):
  XAxJV(AmplifyApp,self).__init__(XAxJC,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,XAxJC,env=XAxJg):
  XAxJV(ElastiCacheCluster,self).__init__(XAxJC,env=env)
class TransferServer(BaseComponent):
 def __init__(self,XAxJC,env=XAxJg):
  XAxJV(TransferServer,self).__init__(XAxJC,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,XAxJC,env=XAxJg):
  XAxJV(CloudFrontDistribution,self).__init__(XAxJC,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,XAxJC,env=XAxJg):
  XAxJV(CodeCommitRepository,self).__init__(XAxJC,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
