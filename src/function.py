import logging, os, json, boto3
import requests
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
from dateutil import tz
from typing import List, Dict, Tuple
import decimal


logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def get_yesterday() -> str:
    return datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

def get_today() -> str:
    return datetime.strftime(datetime.now(), '%Y-%m-%d')

def convertToDict(string: str) -> dict:
    return json.loads(string)

def putS3(bucket: str, key: str, data: str, readers: List[str]) -> dict:
    s3 = boto3.client("s3")
    data = json.dumps(data, cls=DecimalEncoder)
    readers = map(lambda x: "id=" + x, readers)
    readers = ",".join(readers)
    return s3.put_object( Body = data
                        , Bucket = bucket
                        , Key = key
                        , GrantRead = readers
                        )

def get_time_boundaries() -> Tuple[str, str]:
    today = (datetime.now() - timedelta(1)).date()
    start = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
    end = start + timedelta(1)
    return [int(start.timestamp()), int(end.timestamp() + 0.5)]

    
def query(start: str, end: str, table_name: str) -> dict:
    return boto3.resource("dynamodb").Table(table_name) \
            .scan( Select = "ALL_ATTRIBUTES"
                 , FilterExpression = Key("timestamp").between(start, end)
                 )

def lambda_handler(event, context):
    table_name = os.environ["table"]
    bucket = os.environ["bucket"]
    [start, end] = get_time_boundaries()
    res = query(start, end, table_name)
    yesterday = get_yesterday()
    readers = event["read_access_ids"]
    resp = putS3(bucket, yesterday + ".json", res["Items"], readers)
    return resp
