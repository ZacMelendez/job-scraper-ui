import asyncio
import ssl
from typing import List
import aiohttp
import logging

logger = logging.getLogger(__name__)

from .file_types import JobItem

logger = logging.getLogger(__name__)
page_count: int = 15


URL = "https://aexp.eightfold.ai/api/apply/v2/jobs?domain=aexp.com&start={start}&num={num}&domain=aexp.com&sort_by=relevance"
page_count = 10


async def getJobCount(client: aiohttp.ClientSession) -> int:
    logger.info("getting job count for American Express")
    async with client.get(
        "https://aexp.eightfold.ai/careers?intlink=us-amex-career-en-us-home-findalljobs",
        ssl=ssl.SSLContext(),
    ) as response:
        content = await response.text()
        job_count = int(content.split("&#34;count&#34")[1].split(",")[0].split(";:")[1])
        logger.debug(f"{job_count} available jobs on American Express")
        return job_count


async def getAmExJobs(client: aiohttp.ClientSession) -> List[List[JobItem]]:
    jobs_count = await getJobCount(client)
    jobs: List[List[JobItem]] = []
    logger.info(
        "fetching jobs on {} pages for American Express".format(
            round(jobs_count / page_count)
        )
    )
    jobs = await asyncio.gather(
        *[
            getJobsOnPage(client=client, start=10 * i)
            for i in range(round(jobs_count / page_count))
        ]
    )
    logger.info("finished fetching jobs for American Express")
    return jobs


async def getJobsOnPage(client: aiohttp.ClientSession, start: int) -> List[JobItem]:
    jobs: List[JobItem] = []
    logger.debug(f"fetching American Express jobs on page {start/page_count}")
    async with client.get(
        URL.format(start=start, num=page_count), ssl=ssl.SSLContext()
    ) as response:
        data = await response.json()
        amex_jobs = data["positions"]

        for job in amex_jobs:
            in_US = False
            location = (job["location"]).lower()
            if location != "":
                try:
                    if "united states" in location.lower():
                        in_US = True
                except Exception as e:
                    logger.error(job, e)
            if in_US:
                jobs.append(
                    {
                        "company": "American Express".lower(),
                        "job_id": str(job["id"]).lower(),
                        "type": "job",
                        "title": (job["name"]),
                        "search_title": (job["name"]).lower(),
                        "jobUrl": f"https://aexp.eightfold.ai/careers/job?domain=aexp.com&pid={job['id']}&domain=aexp.com&sort_by=relevance&job_index=0".lower(),
                        "location": (job["location"]).lower(),
                    }
                )

        return jobs
