import asyncio
import logging
import ssl
import aiohttp
import json
from enum import Enum
from typing import List, TypedDict, Callable


from .file_types import JobItem


logger = logging.getLogger(__name__)


url = "https://rivian.com/api/gql/content/graphql"
per_page_count = 100


class Pagination(TypedDict):
    total: int
    limit: int
    skip: int


class WorkType(Enum):
    FULL_TIME = "Full-Time"
    N_A = "N/A"
    PART_TIME = "Part-Time"


class Post(TypedDict):
    id: str
    title: str
    location: str
    department: str
    workType: WorkType
    absoluteUrl: str


class PaginatedGreenhouseJobPosts(TypedDict):
    posts: List[Post]
    pagination: Pagination


class Data(TypedDict):
    paginatedGreenhouseJobPosts: PaginatedGreenhouseJobPosts


class RivianGraphQLResponse(TypedDict):
    data: Data


def getQuery(skip: int, limit=per_page_count):
    return {
        "operationName": "CareersPageGreenhouse",
        "variables": {
            "filters": [{"type": "LOCATION", "value": "United States"}],
            "skip": skip,
            "limit": limit,
        },
        "query": """
        query CareersPageGreenhouse($limit: Int, $skip: Int) {
        paginatedGreenhouseJobPosts(
                limit: $limit
                skip: $skip
            ) {
                posts {
                    id
                    title
                    location
                    department
                    workType
                    absoluteUrl
                }
                pagination {
                    total
                    limit
                    skip
                }
            }
        }
        """,
    }


async def getJobCount(client: aiohttp.ClientSession) -> int:
    async with client.post(
        url=url,
        data=json.dumps(getQuery(skip=0)).encode(),
        ssl=ssl.SSLContext(),
        headers={"Content-type": "application/json"},
    ) as response:
        content: RivianGraphQLResponse = await response.json()
        total_jobs = content["data"]["paginatedGreenhouseJobPosts"]["pagination"][
            "total"
        ]
        return total_jobs


rivian_job_parser: Callable[[Post], JobItem] = lambda rivian_post: {
    "company": "rivian",
    "job_id": rivian_post["id"],
    "title": rivian_post["title"],
    "jobUrl": rivian_post["absoluteUrl"],
    "location": rivian_post["location"],
    "type": "job",
    "search_title": rivian_post["title"].lower(),
}


async def getJobsOnPage(client: aiohttp.ClientSession, per_page, page) -> List[JobItem]:
    async with client.post(
        url=url,
        data=json.dumps(getQuery(skip=per_page * page)).encode(),
        ssl=ssl.SSLContext(),
        headers={"Content-type": "application/json"},
    ) as response:
        content: RivianGraphQLResponse = await response.json()
        jobs_on_page = content["data"]["paginatedGreenhouseJobPosts"]["posts"]

        return list(map(rivian_job_parser, jobs_on_page))


async def getRivianJobs(client: aiohttp.ClientSession) -> List[List[JobItem]]:
    jobs_count = await getJobCount(client)
    jobs: List[List[JobItem]] = []
    logger.info(
        "fetching jobs on {} pages for Rivian".format(
            round(jobs_count / per_page_count)
        )
    )
    jobs = await asyncio.gather(
        *[
            getJobsOnPage(client=client, per_page=per_page_count, page=i)
            for i in range(round(jobs_count / per_page_count))
        ]
    )
    logger.info("finished fetching jobs for Rivian")
    return jobs
