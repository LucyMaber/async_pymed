import asyncio
from pymed import PubMed

async def fetch_pubmed_data():
    # Create a PubMed object that GraphQL can use to query
    pubmed = PubMed(tool="MyTool", email="my@email.address")

    # Create a GraphQL query in plain text
    query = "occupational health[Title]"

    # Execute the query against the API asynchronously
    results = await pubmed.query(query, max_results=500)

    # Loop over the retrieved articles
    for article in results:

        # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle)
        print(type(article))

        # Print a JSON representation of the object
        print(article.toJSON())

# Run the async function
asyncio.run(fetch_pubmed_data())
