import asyncio
from pymed import PubMed

async def fetch_and_print_articles(query, max_results):
    # Create a PubMed object that GraphQL can use to query
    # Note that the parameters are not required but kindly requested by PubMed Central
    pubmed = PubMed(tool="MyTool", email="my@email.address")

    # Execute the query against the API
    results = await pubmed.query(query, max_results)

    # Loop over the retrieved articles
    for article in results:
        # Extract and format information from the article
        article_id = article.pubmed_id
        title = article.title
        if article.keywords:
            if None in article.keywords:
                article.keywords.remove(None)
            keywords = '", "'.join(article.keywords)
        publication_date = article.publication_date
        abstract = article.abstract

        # Show information about the article
        print(
            f'{article_id} - {publication_date} - {title}\nKeywords: "{keywords}"\n{abstract}\n'
        )

if __name__ == "__main__":
    query = '(("2018/05/01"[Date - Create] : "3000"[Date - Create])) AND (Xiaoying Xian[Author] OR diabetes)'
    max_results = 500

    # Create and run the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_and_print_articles(query, max_results))
