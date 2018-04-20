#!/usr/bin/env python3

from troposphere import Template, Sub, GetAtt, Ref
from troposphere.s3 import Bucket
from troposphere.codepipeline import Pipeline, ArtifactStore
from awslambdacontinuousdelivery.tools.iam import createCodepipelineRole
from awslambdacontinuousdelivery.source.github import getGitHub
from awslambdacontinuousdelivery.python.test.unittest import getUnittest
from awslambdacontinuousdelivery.python.build import getBuild
from awslambdacontinuousdelivery.deploy import getDeploy
# we will pass the following function to the `getDeploy` function
from awslambdacontinuousdelivery.python.test import getTest
from awslambdacontinuousdelivery.notifications.sns import getEmailTopic 
from awslambdacontinuousdelivery.notifications import addFailureNotifications

template = Template()
# AWS will substitute this with the stack name during deployment
stack_name = Sub("${AWS::StackName}")
source_code = "SourceCode"
deploy_pkg_artifact = "FunctionDeployPackage"
cf_artifact = "CfOutputTemplate"
pipeline_stages = [] # list holding all stages, order matters!
stages = ["Gamma"]

s3 = template.add_resource(
  Bucket("ArtifactStoreS3Location"
        , AccessControl = "Private"
  )
)

pipeline_role = template.add_resource(
  createCodepipelineRole("PipelineRole"))
source = getGitHub(template, source_code)
pipeline_stages.append(source)

unit_tests = getUnittest(template, source_code)
pipeline_stages.append(unit_tests)

build_stage = getBuild(
  template, source_code, deploy_pkg_artifact, cf_artifact, stages)
pipeline_stages.append(build_stage)

for s in stages:
  pipeline_stages.append(getDeploy( template, cf_artifact, s.capitalize(), deploy_pkg_artifact))

PROD = getDeploy(template, cf_artifact, "PROD", deploy_pkg_artifact)

pipeline_stages.append(PROD)

artifact_storage = ArtifactStore( Type = "S3", Location = Ref(s3))
pipeline = Pipeline( "FunctionsPipeline"
                   , Name = Sub("${AWS::StackName}-Pipeline")
                   , RoleArn = GetAtt(pipeline_role, "Arn")
                   , Stages = pipeline_stages
                   , ArtifactStore = artifact_storage
                   )

template.add_resource(pipeline)

#topic = getEmailTopic("Failure Notification", "andy.jassy@amazon.com")
#notification_role = addFailureNotifications(template, Ref(pipeline), topic)

print(template.to_json(indent=2))
