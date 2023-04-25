import asyncio
import json
import time
from typing import Callable, List, TypeVar
import logging
import sys

import aiohttp

from .helpers import (
    amExJobs,
    JobItem,
    capOneJobs,
    paramountJobs,
    bofAJobs,
    rivianJobs,
    put_items,
)


def setup_logging() -> logging.Logger:
    """
    Sets up the logging configuration for the application and returns a logger object.

    Returns:
        logging.Logger: The logger object for the application.
    """
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)

    h = logging.StreamHandler(sys.stdout)

    FORMAT = "[%(levelname)s] %(funcName)s(): %(message)s"
    h.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

    return logger


T = TypeVar("T")


def flatten(list: List[List[T]]) -> List[T]:
    """
    Flattens a list of lists into a single list.

    Args:
        list (List[List[T]]): The list of lists to flatten.

    Returns:
        List[T]: The flattened list.
    """
    return [j for sub in list for j in sub]


def filterJobs(
    jobs: List[List[JobItem]],
) -> List[JobItem]:
    """
    Filters the list of job items based on the given criteria.

    Args:
        jobs (List[List[JobItem]]): The list of job items to filter.
        include (List[str]): The list of keywords to include in the job titles.
        exclude (List[str]): The list of keywords to exclude from the job titles.
        must (List[str]): The list of keywords that must be present in the job titles.

    Returns:
        List[JobItem]: The list of job items that match the filtering criteria.
    """
    flat = flatten(jobs)
    unique = list({v["jobUrl"]: v for v in flat}.values())

    return unique


async def run_scrape(logger: logging.Logger, scraper: Callable) -> List[List[JobItem]]:
    """
    Runs the given scraper function and returns the scraped job items.

    Args:
        logger (logging.Logger): The logger object for the application.
        scraper (Callable): The scraper function to run.

    Returns:
        List[List[JobItem]]: The list of job items scraped by the scraper function.
    """
    logger.info(f"starting scraper {scraper.__name__}")
    async with aiohttp.ClientSession() as client:
        try:
            jobs = await scraper(client=client)

            logger.info(f"finished scraping {scraper.__name__}")
            return jobs
        except Exception as e:
            logger.error(e)
            return []


async def main(logger: logging.Logger) -> List[List[JobItem]]:
    """
    Runs the scrapers for Capital One and Paramount and returns the scraped job items.

    Args:
        logger (logging.Logger): The logger object for the application.

    Returns:
        List[List[JobItem]]: The list of job items scraped by both scrapers.
    """
    logger.info("starting scraper")
    try:
        coJobs: List[List[JobItem]]
        parJobs: List[List[JobItem]]
        amexJobs: List[List[JobItem]]
        bofaJobs: List[List[JobItem]]
        rivJobs: List[List[JobItem]]
        [coJobs, parJobs, amexJobs, bofaJobs, rivJobs] = await asyncio.gather(
            *[
                run_scrape(logger, capOneJobs),
                run_scrape(logger, paramountJobs),
                run_scrape(logger, amExJobs),
                run_scrape(logger, bofAJobs),
                run_scrape(logger, rivianJobs),
            ]
        )
        return [*coJobs, *parJobs, *amexJobs, *bofaJobs, *rivJobs]
    except Exception as e:
        logger.error(e)
        return []


def lambda_handler(event, context):
    """
        The AWS Lambda function handler for the application.

    Args:
        event (ApiGatewayEvent): The AWS API Gateway event object.
        context (dict): The AWS Lambda context object.

    Returns:
        dict: The API Gateway response object containing the scraped job items.
    """
    logger = setup_logging()
    try:
        start = time.perf_counter()
        jobs = asyncio.run(main(logger))
        end = time.perf_counter()
        filtered_jobs = filterJobs(jobs)

        logger.info(f"found {len(filtered_jobs)} jobs in {end - start:0.4f} seconds")

        logger.info(f"putting jobs in dynamodb")
        asyncio.run(put_items(filtered_jobs))
        logger.info(f"successfully put {len(filtered_jobs)} items in DynamoDB")

        return
    except Exception as e:
        logger.error(e)
        return
