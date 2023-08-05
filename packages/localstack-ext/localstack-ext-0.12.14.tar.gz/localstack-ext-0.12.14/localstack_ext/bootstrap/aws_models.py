from localstack.utils.aws import aws_models
yhLxn=super
yhLxk=None
yhLxa=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  yhLxn(LambdaLayer,self).__init__(arn)
  self.cwd=yhLxk
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.yhLxa.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,yhLxa,env=yhLxk):
  yhLxn(RDSDatabase,self).__init__(yhLxa,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,yhLxa,env=yhLxk):
  yhLxn(RDSCluster,self).__init__(yhLxa,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,yhLxa,env=yhLxk):
  yhLxn(AppSyncAPI,self).__init__(yhLxa,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,yhLxa,env=yhLxk):
  yhLxn(AmplifyApp,self).__init__(yhLxa,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,yhLxa,env=yhLxk):
  yhLxn(ElastiCacheCluster,self).__init__(yhLxa,env=env)
class TransferServer(BaseComponent):
 def __init__(self,yhLxa,env=yhLxk):
  yhLxn(TransferServer,self).__init__(yhLxa,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,yhLxa,env=yhLxk):
  yhLxn(CloudFrontDistribution,self).__init__(yhLxa,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,yhLxa,env=yhLxk):
  yhLxn(CodeCommitRepository,self).__init__(yhLxa,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
