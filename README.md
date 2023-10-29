# PyMed - Asynchronous PubMed Access through Python

PyMed is an asynchronous Python library that provides access to PubMed through the PubMed API.

**IMPORTANT NOTE**: The PubMed API needs to be well-documented and can be challenging. This library simplifies the process of querying PubMed, making it easier to retrieve data.

## Why this library?

The PubMed API needs to be more well documented, and querying it in a performant way can be complicated and time-consuming. This asynchronous wrapper provides access to the API in a consistent, readable, and performant way, especially when dealing with many requests concurrently.

## Features

This library includes the following features:

- Asynchronous querying of the PubMed database using the standard PubMed query language.
- Batching of requests for better performance.
- Parsing and cleaning of the retrieved articles.
- Conforms to the PubMed API guidelines for rate limiting and identification.

## Examples

For full working examples, take a look at the `examples/` folder in this repository. In essence, you can import the `PubMed` class, instantiate it, and use it to query PubMed data asynchronously:

```python
import asyncio
from pymed import PubMed

async def fetch_pubmed_data():
    # Create a PubMed object
    pubmed = PubMed(tool="MyTool", email="my@email.address")

    # Define your query
    query = "Some query"

    # Execute the query asynchronously
    results = await pubmed.query(query, max_results=500)

    # Process the retrieved data
    for article in results:
        print(type(article))
        print(article.toJSON())

# Run the async function
asyncio.run(fetch_pubmed_data())
```

## Notes on the API

The original documentation of the PubMed API can be found here: [PubMed Central](https://www.ncbi.nlm.nih.gov/pmc/tools/developers/). When using this library, please adhere to the following guidelines:

- Do not make concurrent requests, even at off-peak times.
- Include two parameters to identify your application to the servers:
  - `tool`: The name of your application, as a string value with no internal spaces.
  - `email`: The email address of the maintainer of the tool, which should be a valid email address.

## Notice of Non-Affiliation and Disclaimer

The author of this library is not affiliated, associated, authorized, endorsed by, or officially connected with PubMed, or any of its subsidiaries or affiliates. The official PubMed website can be found at [https://www.ncbi.nlm.nih.gov/pubmed/](https://www.ncbi.nlm.nih.gov/pubmed/).

**Please note**: This library is provided as-is, and the author may not actively maintain it. You are encouraged to create a fork or use the code for your own projects. Thank you to all contributors and users!
