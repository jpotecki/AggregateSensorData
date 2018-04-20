import unittest, os, sys, json, logging
import boto3
from moto import mock_dynamodb2
from moto.dynamodb import dynamodb_backend
from moto import mock_s3

testdir = os.path.dirname(__file__)
srcdir = '../../src'
src = os.path.join(testdir, srcdir)
sys.path.insert(0, os.path.abspath(src))
import function as f



class S3Tests(unittest.TestCase):
    @mock_s3
    def test_putS3(self):
        bucket = "testbucket"
        key = "testkey"
        data = "testdata"
        readers = [ "1a", "2b", "3k" ]
        conn = boto3.resource("s3")
        conn.create_bucket( Bucket = bucket )
        
        # let us run the test
        res = f.putS3(bucket, key, data, readers)
        
        obj = conn.Object(bucket, key)
        self.assertNotEqual(obj, None)
    
    @mock_dynamodb2
    def test_query(self):
        db = boto3.client("dynamodb")
        table_name = "test"
        hash_name = "sensorId"
        sort_key = "timestamp"

        # create table
        db.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': hash_name,
                    'AttributeType': "N"
                },
                {
                    'AttributeName': sort_key,
                    'AttributeType': "N"
                }
            ],
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': hash_name,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': sort_key,
                    'KeyType': 'RANGE'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 123,
                'WriteCapacityUnits': 123
            }
        )
        item = db.put_item(
            TableName = table_name,
            Item = { hash_name : {"N": "1"}, sort_key: {"N": "2"} }
            )
        self.assertNotEqual(item, None)

        # now see if we get it
        resp = f.query("1", "3", table_name)
        self.assertEqual(resp["Count"], 1)
        resp = f.query("4", "9", table_name)
        self.assertEqual(resp["Count"], 0)

if __name__ == "__main__":
    unittest.main()
