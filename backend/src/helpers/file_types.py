import asyncio
from typing import TypedDict, Dict, Optional
from uuid import UUID


class JobItem(TypedDict):
    company: str
    job_id: str
    title: str
    url: str


class PathParameters(TypedDict):
    proxy: str


class RequestContext(TypedDict):
    accountId: str
    resourceId: int
    stage: str
    requestId: UUID
    requestTime: str
    request_time_epoch: int
    identity: Dict[str, Optional[str]]
    path: str
    resourcePath: str
    httpMethod: str
    apiId: int
    protocol: str


class StageVariables(TypedDict):
    baz: str


class ApiGatewayEvent(TypedDict):
    body: str
    resource: str
    path: str
    httpMethod: str
    isBase64Encoded: bool
    queryStringParameters: Dict[str, str]
    pathParameters: PathParameters
    stageVariables: StageVariables
    headers: Dict[str, str]
    requestContext: RequestContext
