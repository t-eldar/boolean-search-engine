from itertools import takewhile
import os
from os.path import join
from file_utils import DEFAULT_BASE_PATH, read_text_from_file, save_text
from wiki_crawler.content_crawler import ContentCrawler


def download_wiki_texts(category):
    download_path = DEFAULT_BASE_PATH
    base_url = f"https://ru.wikipedia.org/wiki/Категория:{category}"


    path = join(download_path, "texts", category)
    if os.path.exists(path):
        files = os.listdir(path)
        if len(files) >= 100:
            os.chdir(path)
            texts = []
            for f in files:
                texts.append(
                    (
                        read_text_from_file(join(path, f)),
                        int("".join(list(takewhile(lambda c: c != ".", f)))),
                    )
                )

            return texts

    crawler = ContentCrawler(
        on_save=lambda content, num: save_text(content, num, category)
    )

    texts = crawler.crawl_category(base_url)

    return texts


if __name__ == "__main__":
    download_wiki_texts("История_народов")
