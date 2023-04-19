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
    ApiGatewayEvent,
    capOneJobs,
    paramountJobs,
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
    include: List[str],
    exclude: List[str],
    must: List[str],
    locations: List[str],
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

    return list(
        filter(
            lambda job: (
                True
                if not len(must)
                else all(title.lower() in job["title"].lower() for title in must)
            )
            and (
                True
                if not len(include)
                else any(title.lower() in job["title"].lower() for title in include)
            )
            and not (
                False
                if not len(exclude)
                else any(title.lower() in job["title"].lower() for title in exclude)
            )
            and (
                True
                if not len(locations)
                else any(
                    location.lower() in job["location"].lower()
                    for location in locations
                )
            ),
            flat,
        )
    )


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
        [coJobs, parJobs, amexJobs] = await asyncio.gather(
            *[
                run_scrape(logger, capOneJobs),
                run_scrape(logger, paramountJobs),
                run_scrape(logger, amExJobs),
            ]
        )
        return [*coJobs, *parJobs, *amexJobs]
    except Exception as e:
        logger.error(e)
        return []


def lambda_handler(event: ApiGatewayEvent, context):
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
        include: List[str] = []
        exclude: List[str] = []
        must: List[str] = []
        locations: List[str] = []
        store: bool = False
        if event["queryStringParameters"]:
            queries = event["queryStringParameters"]
            if "include" in queries:
                include = [item.strip() for item in queries["include"].split(",")]
            if "exclude" in queries:
                exclude = [item.strip() for item in queries["exclude"].split(",")]
            if "must" in queries:
                must = [item.strip() for item in queries["must"].split(",")]
            if "locations" in queries:
                locations = [item.strip() for item in queries["locations"].split(",")]
            if "store" in queries:
                store = queries["store"].lower() == "true"

        start = time.perf_counter()
        jobs = asyncio.run(main(logger))
        end = time.perf_counter()
        filtered_jobs = filterJobs(jobs, include, exclude, must, locations)

        logger.info(f"found {len(filtered_jobs)} jobs in {end - start:0.4f} seconds")

        if store:
            logger.info(f"putting jobs in dynamodb")
            result = asyncio.run(put_items(filtered_jobs))
            successful = list(
                filter(
                    lambda response: response["ResponseMetadata"]["HTTPStatusCode"]
                    < 400,
                    result,
                )
            )
            logger.info(f"successfully put {len(successful)} items in DynamoDB")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
            },
            "body": json.dumps(
                {"info": list({v["url"]: v for v in filtered_jobs}.values())}
            ),
        }
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
            },
            "body": json.dumps({"info": "internal server error, please check logs"}),
        }
