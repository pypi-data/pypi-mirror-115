from localstack.utils.aws import aws_models
vrEbh=super
vrEbc=None
vrEbM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  vrEbh(LambdaLayer,self).__init__(arn)
  self.cwd=vrEbc
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.vrEbM.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,vrEbM,env=vrEbc):
  vrEbh(RDSDatabase,self).__init__(vrEbM,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,vrEbM,env=vrEbc):
  vrEbh(RDSCluster,self).__init__(vrEbM,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,vrEbM,env=vrEbc):
  vrEbh(AppSyncAPI,self).__init__(vrEbM,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,vrEbM,env=vrEbc):
  vrEbh(AmplifyApp,self).__init__(vrEbM,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,vrEbM,env=vrEbc):
  vrEbh(ElastiCacheCluster,self).__init__(vrEbM,env=env)
class TransferServer(BaseComponent):
 def __init__(self,vrEbM,env=vrEbc):
  vrEbh(TransferServer,self).__init__(vrEbM,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,vrEbM,env=vrEbc):
  vrEbh(CloudFrontDistribution,self).__init__(vrEbM,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,vrEbM,env=vrEbc):
  vrEbh(CodeCommitRepository,self).__init__(vrEbM,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
