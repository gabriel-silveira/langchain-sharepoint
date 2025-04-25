from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import dotenv_values

config = dotenv_values(".env")


class WebCrawler:
    __url: str
    __limit: int

    def __init__(self, url: str = '', limit=1):
        self.__url = url
        self.__limit = limit

    def start(self):
        result = self.__crawl_url()

        return result

    def __crawl_url(self):
        app = FirecrawlApp(api_key=config['FIRECRAWL_API_KEY'])

        print(f'Starting crawling {self.__url} with limit {self.__limit}')

        # Crawl a website:
        crawled_results = app.crawl_url(
            self.__url,
            limit=self.__limit,
            scrape_options=ScrapeOptions(formats=['markdown']),
            poll_interval=30
        )

        results: dict = {}

        if crawled_results.status == "completed":
            print('Crawling completed!')

            print('Writing markdown files...')

            for doc in crawled_results.data:
                with open(f'crawled/{doc.metadata['scrapeId']}.txt', "wb") as f:
                    f.write(doc.markdown.encode())

                    results[doc.metadata['scrapeId']] = {
                        'url': doc.metadata['url'],
                        'markdown': doc.markdown,
                    }

        print('Markdown files written')

        print('Returning results')

        return results

        # for i, crawled in enumerate(crawled_results):
        #    print(f'Section {i}')
        #    print(crawled)
