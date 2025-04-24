from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import dotenv_values

config = dotenv_values(".env")


def crawl_url(url: str):
    app = FirecrawlApp(api_key=config['FIRECRAWL_API_KEY'])

    # Crawl a website:
    crawled_results = app.crawl_url(
        url,
        limit=1,
        scrape_options=ScrapeOptions(formats=['markdown']),
        poll_interval=30
    )

    if crawled_results.status == "completed":
        for doc in crawled_results.data:
            print(doc.markdown)

            with open(f'crawled/{doc.metadata['scrapeId']}.txt', "wb") as f:
                f.write(doc.markdown.encode())

    # for i, crawled in enumerate(crawled_results):
    #    print(f'Section {i}')
    #    print(crawled)


website = "https://www.csn.com.br/"

crawl_url(website)
