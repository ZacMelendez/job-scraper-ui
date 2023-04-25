import asyncio
import ssl
from typing import List
import aiohttp
import logging

logger = logging.getLogger(__name__)

from .file_types import JobItem


URL = "https://careers.bankofamerica.com/services/jobssearchservlet?start={start}&rows={page_count}&search=getAllJobs"
page_count: int = 10


async def getJobCount(client: aiohttp.ClientSession) -> int:
    logger.info("getting job count for Bank of America")
    async with client.get(
        "https://careers.bankofamerica.com/services/jobssearchservlet?start=0&rows=10&search=getAllJobs",
        ssl=ssl.SSLContext(),
    ) as response:
        content = await response.json()
        job_count = int(content["totalMatches"])
        logger.debug(f"{job_count} available jobs on Bank of America")
        return job_count


async def getBofAJobs(client: aiohttp.ClientSession) -> List[List[JobItem]]:
    await asyncio.sleep(0.5)
    jobs_count = await getJobCount(client)
    jobs: List[List[JobItem]] = []
    logger.info(
        "fetching jobs on {} pages for Bank of America".format(
            round(jobs_count / page_count)
        )
    )
    jobs = await asyncio.gather(
        *[
            getJobsOnPage(client=client, start=page_count * i)
            for i in range(round(jobs_count / page_count))
        ]
    )
    logger.info("finished fetching jobs for Bank of America")
    return jobs


async def getJobsOnPage(client: aiohttp.ClientSession, start: int) -> List[JobItem]:
    jobs: List[JobItem] = []
    logger.debug(f"fetching Bank of America jobs on page {start/page_count}")
    async with client.get(
        URL.format(start=start, page_count=start + page_count), ssl=ssl.SSLContext()
    ) as response:
        data = await response.json()
        bofa_jobs = data["jobsList"]

        for job in bofa_jobs:
            url = job["jcrURL"]
            in_US = False
            country = job["country"]
            if country != "":
                try:
                    if "united states" in country.lower():
                        in_US = True
                except Exception as e:
                    logger.error(job, e)
            if in_US:
                jobs.append(
                    {
                        "company": "Bank of America".lower(),
                        "job_id": str(job["jobRequisitionId"]).lower(),
                        "type": "job",
                        "title": (job["postingTitle"]),
                        "search_title": (job["postingTitle"]).lower(),
                        "jobUrl": f"https://careers.bankofamerica.com{url}".lower(),
                        "location": (job["location"]).lower(),
                    }
                )

        return jobs
