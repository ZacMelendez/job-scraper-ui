import asyncio
from typing import TypedDict, Dict, Optional
from uuid import UUID


class JobItem(TypedDict):
    company: str
    job_id: str
    title: str
    jobUrl: str
    location: str
    type: str


class States:
    def __init__(self):
        self.abbreviations = [
            "AL",
            "AK",
            "AS",
            "AZ",
            "AR",
            "CA",
            "CO",
            "CT",
            "DE",
            "DC",
            "FM",
            "FL",
            "GA",
            "GU",
            "HI",
            "ID",
            "IL",
            "IN",
            "IA",
            "KS",
            "KY",
            "LA",
            "ME",
            "MH",
            "MD",
            "MA",
            "MI",
            "MN",
            "MS",
            "MO",
            "MT",
            "NE",
            "NV",
            "NH",
            "NJ",
            "NM",
            "NY",
            "NC",
            "ND",
            "MP",
            "OH",
            "OK",
            "OR",
            "PW",
            "PA",
            "PR",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VT",
            "VI",
            "VA",
            "WA",
            "WV",
            "WI",
            "WY",
        ]
        self.states = [
            "Alabama",
            "Alaska",
            "Arizona",
            "Arkansas",
            "California",
            "Colorado",
            "Connecticut",
            "Delaware",
            "Florida",
            "Georgia",
            "Hawaii",
            "Idaho",
            "Illinois",
            "Indiana",
            "Iowa",
            "Kansas",
            "Kentucky",
            "Louisiana",
            "Maine",
            "Maryland",
            "Massachusetts",
            "Michigan",
            "Minnesota",
            "Mississippi",
            "Missouri",
            "Montana",
            "Nebraska",
            "Nevada",
            "New Hampshire",
            "New Jersey",
            "New Mexico",
            "New York",
            "North Carolina",
            "North Dakota",
            "Ohio",
            "Oklahoma",
            "Oregon",
            "Pennsylvania",
            "Rhode Island",
            "South Carolina",
            "South Dakota",
            "Tennessee",
            "Texas",
            "Utah",
            "Vermont",
            "Virginia",
            "Washington",
            "West Virginia",
            "Wisconsin",
            "Wyoming",
        ]


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
