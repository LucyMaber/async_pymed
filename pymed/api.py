import datetime
import itertools
import xml.etree.ElementTree as xml
from typing import Union

import aiohttp
import asyncio

from .helpers import batches
from .article import PubMedArticle
from .book import PubMedBookArticle

BASE_URL = "https://eutils.ncbi.nlm.nih.gov"

class PubMed(object):
    def __init__(
        self, tool: str = "my_tool", email: str = "my_email@example.com"
    ):
        self.tool = tool
        self.email = email
        self._rateLimit = 3
        self._requestsMade = []
        self.parameters = {"tool": tool, "email": email, "db": "pubmed"}

    async def query(self, query: str, max_results: int = 100):
        article_ids = self._getArticleIds(query=query, max_results=max_results)
        articles = await asyncio.gather(
            *[
                self._getArticles(article_ids=batch)
                for batch in batches(article_ids, 250)
            ]
        )
        return list(itertools.chain.from_iterable(articles))

    def getTotalResultsCount(self, query: str) -> int:
        parameters = self.parameters.copy()
        parameters["term"] = query
        parameters["retmax"] = 1
        response = self._get(url="/entrez/eutils/esearch.fcgi", parameters=parameters)
        total_results_count = int(response.get("esearchresult", {}).get("count"))
        return total_results_count

    def _exceededRateLimit(self) -> bool:
        self._requestsMade = [
            requestTime
            for requestTime in self._requestsMade
            if requestTime > datetime.datetime.now() - datetime.timedelta(seconds=1)
        ]
        return len(self._requestsMade) > self._rateLimit

    async def _get(self, url: str, parameters: dict, output: str = "json") -> Union[dict, str]:
        while self._exceededRateLimit():
            await asyncio.sleep(1)
        parameters["retmode"] = output
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}{url}", params=parameters) as response:
                response.raise_for_status()
                self._requestsMade.append(datetime.datetime.now())
                if output == "json":
                    return await response.json()
                else:
                    return await response.text()

    async def _getArticles(self, article_ids: list):
        parameters = self.parameters.copy()
        parameters["id"] = article_ids
        response = await self._get(url="/entrez/eutils/efetch.fcgi", parameters=parameters, output="xml")
        root = xml.fromstring(response)
        for article in root.iter("PubmedArticle"):
            yield PubMedArticle(xml_element=article)
        for book in root.iter("PubmedBookArticle"):
            yield PubMedBookArticle(xml_element=book)

    def _getArticleIds(self, query: str, max_results: int) -> list:
        article_ids = []
        parameters = self.parameters.copy()
        parameters["term"] = query
        parameters["retmax"] = 50000
        if max_results < parameters["retmax"]:
            parameters["retmax"] = max_results
        response = self._get(url="/entrez/eutils/esearch.fcgi", parameters=parameters)
        article_ids += response.get("esearchresult", {}).get("idlist", [])
        total_result_count = int(response.get("esearchresult", {}).get("count"))
        retrieved_count = int(response.get("esearchresult", {}).get("retmax"))
        if max_results == -1:
            max_results = total_result_count
        while retrieved_count < total_result_count and retrieved_count < max_results:
            if (max_results - retrieved_count) < parameters["retmax"]:
                parameters["retmax"] = max_results - retrieved_count
            parameters["retstart"] = retrieved_count
            response = self._get(url="/entrez/eutils/esearch.fcgi", parameters=parameters)
            article_ids += response.get("esearchresult", {}).get("idlist", [])
            retrieved_count += int(response.get("esearchresult", {}).get("retmax"))
        return article_ids
