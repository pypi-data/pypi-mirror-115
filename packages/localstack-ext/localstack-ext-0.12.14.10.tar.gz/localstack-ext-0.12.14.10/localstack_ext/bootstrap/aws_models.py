from localstack.utils.aws import aws_models
XtbRJ=super
XtbRg=None
XtbRi=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  XtbRJ(LambdaLayer,self).__init__(arn)
  self.cwd=XtbRg
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.XtbRi.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,XtbRi,env=XtbRg):
  XtbRJ(RDSDatabase,self).__init__(XtbRi,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,XtbRi,env=XtbRg):
  XtbRJ(RDSCluster,self).__init__(XtbRi,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,XtbRi,env=XtbRg):
  XtbRJ(AppSyncAPI,self).__init__(XtbRi,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,XtbRi,env=XtbRg):
  XtbRJ(AmplifyApp,self).__init__(XtbRi,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,XtbRi,env=XtbRg):
  XtbRJ(ElastiCacheCluster,self).__init__(XtbRi,env=env)
class TransferServer(BaseComponent):
 def __init__(self,XtbRi,env=XtbRg):
  XtbRJ(TransferServer,self).__init__(XtbRi,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,XtbRi,env=XtbRg):
  XtbRJ(CloudFrontDistribution,self).__init__(XtbRi,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,XtbRi,env=XtbRg):
  XtbRJ(CodeCommitRepository,self).__init__(XtbRi,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
