from firecrawl import FirecrawlApp, ScrapeOptions
from langchain_openai import OpenAIEmbeddings
from dotenv import dotenv_values

config = dotenv_values(".env")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


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

                # TODO
                ## Check the course "LangChain Chat with Your Data" - Lesson 3: Document Splitting

                # Context aware splitting

                # Chunking aims to keep text with common context together.
                # A text splitting often uses sentences or other delimiters
                # to keep related text together but many documents
                # (such as Markdown) have structure (headers) that can be
                # explicitly used in splitting.

                # We can use `MarkdownHeaderTextSplitter` to preserve
                # header metadata in our chunks, as show below.

                # TODO
                ## Insert markdowns (chunks) into Milvus
                ## See: insert_markdown_data(collection, markdown_fragments)

        print('Markdown files written')

        print('Returning results')

        return results

        # for i, crawled in enumerate(crawled_results):
        #    print(f'Section {i}')
        #    print(crawled)


# Função para gerar embeddings
def generate_embeddings(markdown_fragments):
    return embedding_model.embed_documents(markdown_fragments)


def insert_markdown_data(collection, markdown_fragments):
    # Gerar embeddings
    embeddings = generate_embeddings(markdown_fragments)

    # Preparar dados para inserção
    entities = [
        {"content": markdown_fragments},
        {"embedding": embeddings}
    ]

    # Inserir no Milvus
    collection.insert(entities)
    collection.flush()  # Garantir que os dados são persistidos

    print(f"Inseridos {len(markdown_fragments)} fragmentos no Milvus")
