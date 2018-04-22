from awslambdacontinuousdelivery.tools.iam import (
    defaultAssumeRolePolicyDocument
  , oneClickCreateLogsPolicy
  )

from troposphere import Sub
from troposphere.iam import Role, Policy
from awacs.dynamodb import GetItem, GetRecords, Scan, Query
import awacs.aws
import awacs.s3 as s3

def get_dynamodb_access() -> Policy:
  statements = [
    awacs.aws.Statement(
      Action = [ GetItem, GetRecords, Scan, Query ],
      Effect = awacs.aws.Allow,
      Resource = [ Sub("arn:aws:dynamodb:${AWS::Region}:${AWS::AccountId}:table/IoTSensorDataGamma") ]
    )
  ]
  policyDoc = awacs.aws.Policy( Statement = statements )
  return Policy( PolicyName = Sub("DynamoDbGammaAccess-${AWS::StackName}")
               , PolicyDocument = policyDoc
               )


def get_s3_access() -> Policy:
  statements = [
    awacs.aws.Statement(
      Action = [ s3.PutObject, s3.PutObjectAcl ],
      Effect = awacs.aws.Allow,
      Resource = [ "arn:aws:s3:::example-aggregatedsensordata-gamma/*" ]
    )
  ]
  policyDoc = awacs.aws.Policy( Statement = statements )
  return Policy( PolicyName = Sub("S3Access-${AWS::StackName}")
               , PolicyDocument = policyDoc
               )

def get_iam(ref_name: str) -> Role:
  assume = defaultAssumeRolePolicyDocument("lambda.amazonaws.com")
  return Role( ref_name
             , RoleName = ref_name
             , AssumeRolePolicyDocument = assume
             , Policies = [ oneClickCreateLogsPolicy()
                          , get_s3_access()
                          , get_dynamodb_access()
                          ]
             )

if __name__ == "__main__":
  print("For Testing only")
  secret = get_secret_manager()
  print(str(secret.to_dict()))
  role = get_iam("Test")
  print(str(role.to_dict()))
