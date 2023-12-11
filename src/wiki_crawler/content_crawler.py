import requests
from bs4 import BeautifulSoup


class ContentCrawler:
    def __init__(self, on_save):
        self.on_save = on_save

    __downloaded_texts = 0
    __visited_urls = set()
    __text_number = 1
    __texts = []

    def reset(self):
        self.__downloaded_texts = 0
        self.__visited_urls = 0
        self.__text_number = 1
        self.__texts = []

    def crawl_page(self, url):
        paragraphs_to_download = 4
        if self.__downloaded_texts >= 100:
            return

        if url in self.__visited_urls:
            return
        self.__visited_urls.add(url)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Находим текст статьи и сохраняем его
            content_div = soup.find("div", {"class": "mw-parser-output"})
            if content_div:
                paragraphs = content_div.find_all("p")
                text_content = ""
                p_count = 0
                for paragraph in paragraphs:
                    # Игнорируем текст из таблиц
                    if paragraph.find_parents("table"):
                        continue
                    text_content += paragraph.text + "\n"
                    p_count += 1
                    if p_count >= paragraphs_to_download:
                        break

                if text_content != "":
                    self.__texts.append((text_content, self.__text_number))
                    self.on_save(text_content, self.__text_number)
                    self.__downloaded_texts += 1
                    self.__text_number += 1

        except requests.RequestException as e:
            print(f"Ошибка при запросе страницы {url}: {e}")

    def crawl_category(self, url):
        if self.__downloaded_texts >= 100:
            return self.__texts

        if url in self.__visited_urls:
            return self.__texts
        self.__visited_urls.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Находим страницы с контентом
            pages_div = soup.find("div", {"id": "mw-pages"})
            if pages_div:
                content_div = pages_div.find("div", {"class": "mw-content-ltr"})
                links = content_div.find_all("a", href=True)
                for link in links:
                    href = link["href"]
                    if href.startswith("/wiki/") and ":" not in href:
                        new_url = f"https://ru.wikipedia.org{href}"

                        self.crawl_page(new_url)
                        print("crawled page " + new_url)

            # Находим подкатегории
            categories_div = soup.find("div", {"id": "mw-subcategories"})
            if categories_div:
                content_div = categories_div.find("div", {"class": "mw-content-ltr"})
                links = content_div.find_all("a", href=True)

                for link in links:
                    href = link["href"]
                    if href.startswith("/wiki/"):
                        new_url = f"https://ru.wikipedia.org{href}"

                        self.crawl_category(new_url)
                        print("crawled category " + new_url)
        except requests.RequestException as e:
            print(f"Ошибка при запросе страницы {url}: {e}")

        return self.__texts
