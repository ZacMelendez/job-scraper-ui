import os
from typing import List, TypedDict
import aioboto3
from .file_types import JobItem


class HTTPHeaders(TypedDict):
    server: str
    date: str
    content_type: str
    content_length: int
    connection: str
    x_amzn_requestid: str
    x_amz_crc32: str


class ResponseMetadata(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: HTTPHeaders
    RetryAttempts: int


class Response(TypedDict):
    ResponseMetadata: ResponseMetadata


async def put_items(jobs: List[JobItem]):
    session = aioboto3.Session(region_name="us-east-1")
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table(os.environ.get("JOBS_TABLE") or "")
        async with table.batch_writer() as batch_writer:
            for job in jobs:
                await batch_writer.put_item(Item=job)
