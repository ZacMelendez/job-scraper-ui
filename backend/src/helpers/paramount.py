import asyncio
import ssl
import time
from typing import List
from bs4 import BeautifulSoup
import aiohttp
from typing import List
import logging

from .file_types import JobItem

logger = logging.getLogger(__name__)

page_count: int = 25
URL = "https://careers.paramount.com/tile-search-results/?q=developer&startrow={start_row}&_=1678893069634"


async def getJobCount(client: aiohttp.ClientSession) -> int:
    logger.info("getting job count for Paramount")
    async with client.get(
        "https://careers.paramount.com/search/?createNewAlert=false&q=developer&locationsearch=&optionsFacetsDD_customfield1=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield3=",
        ssl=ssl.SSLContext(),
    ) as response:
        content = await response.text()
        soup = BeautifulSoup(content, features="html.parser")

        jobs_count = 0

        jobs_count_search = soup.select("span#tile-search-results-label")[0]
        if jobs_count_search:
            jobs_count = int(jobs_count_search.text.split(" ")[5])

        return jobs_count


async def getParamountJobs(client: aiohttp.ClientSession) -> List[List[JobItem]]:
    jobs_count = await getJobCount(client)
    jobs: List[List[JobItem]] = []
    logger.info("fetching all Paramount jobs")

    jobs = await asyncio.gather(
        *[
            getJobsOnPage(client=client, page=i)
            for i in range(round(jobs_count / page_count))
        ]
    )
    logger.info("finished fetching all Paramount jobs")
    return jobs


async def getJobsOnPage(client: aiohttp.ClientSession, page: int) -> List[JobItem]:
    jobs: List[JobItem] = []
    logger.debug(f"fetching Paramount jobs on page {page}")
    async with client.get(
        URL.format(start_row=page * page_count), ssl=ssl.SSLContext()
    ) as response:
        content = await response.text()
        soup = BeautifulSoup(content, features="html.parser")
        jobs_search = soup.select("li.job-tile")
        if jobs_search:
            for job in jobs_search:
                try:
                    title_search = job.select("a.jobTitle-link")
                    title = ""
                    job_id = ""
                    href = ""
                    location = ""

                    location_search = job.find("div", "location-value")

                    if location_search:
                        location = location_search.text

                    if len(title_search):
                        job_tile = title_search[0]

                        title = job_tile.text.strip()
                        job_id = job_tile.attrs["data-focus-tile"].split("-")[-1]
                        href = job_tile.attrs["href"]

                    if title != "":
                        jobs.append(
                            {
                                "company": "Paramount",
                                "job_id": job_id,
                                "title": title,
                                "url": f"https://careers.paramount.com{href}",
                                "location": location,
                            }
                        )
                except Exception as e:
                    print(job, e)
        return jobs