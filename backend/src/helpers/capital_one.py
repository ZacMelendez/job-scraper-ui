import asyncio
import json
import ssl
import time
from typing import List
from bs4 import BeautifulSoup
import aiohttp
import logging

logger = logging.getLogger(__name__)

from .file_types import JobItem

URL: str = "https://www.capitalonecareers.com/search-jobs/results?ActiveFacetID=0&CurrentPage={page}&RecordsPerPage=15&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=True&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&Postal"
page_count: int = 15


async def getJobCount(client: aiohttp.ClientSession) -> int:
    logger.info("getting job count for Capital One")
    async with client.get(URL.format(page=1), ssl=ssl.SSLContext()) as response:
        content = await response.json()
        soup = BeautifulSoup(content["results"], features="html.parser")

        jobs_count = 0

        jobs_count_search = soup.select("div.search-results-intro")[0].find("h1")
        if jobs_count_search:
            jobs_count = int(jobs_count_search.text.split(" ")[0])

        return jobs_count


async def getCapitalOneJobs(client: aiohttp.ClientSession) -> List[List[JobItem]]:
    jobs_count = await getJobCount(client)
    jobs: List[List[JobItem]] = []
    logger.info(
        "fetching jobs on {} pages for Capital One".format(
            round(jobs_count / page_count)
        )
    )
    jobs = await asyncio.gather(
        *[
            getJobsOnPage(client=client, page=i)
            for i in range(round(jobs_count / page_count))
        ]
    )
    logger.info("finished fetching jobs for Capital One")
    return jobs


async def getJobsOnPage(client: aiohttp.ClientSession, page: int) -> List[JobItem]:
    jobs: List[JobItem] = []
    logger.debug(f"fetching Capital One jobs on page {page}")
    async with client.get(
        URL.format(page=page, page_count=page_count), ssl=ssl.SSLContext()
    ) as response:
        data = await response.json()
        soup = BeautifulSoup(data["results"], features="html.parser")
        jobs_search = soup.select("a[data-job-id]")
        if jobs_search:
            for job in jobs_search:
                try:
                    job_id = job.attrs["data-job-id"].replace('\\"', "")
                    href = job.attrs["href"]
                    title = ""
                    title_search = job.find("h2")
                    if title_search:
                        title = title_search.text
                    location = ""
                    location_search = job.find("span", "job-location")
                    if location_search:
                        location = location_search.text
                    if title != "":
                        jobs.append(
                            {
                                "company": "Capital One",
                                "job_id": job_id,
                                "title": title,
                                "url": f"https://www.capitalonecareers.com{href}",
                                "location": location,
                            }
                        )
                except Exception as e:
                    print(job, e)
        return jobs
