import pandas as pd
import requests
import math
from bs4 import BeautifulSoup


class ScraperError(Exception):
    pass


class eBay:
    """
        Holds everything related to extracting the relevant information
        from the website of interest.
    """
    def __init__(self):
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
        self.__dataframe = None
        self.__keyword = None
        self.__productlist = None

    def scrape(self, keyword: str, quantity: int) -> pd.DataFrame:
        """
        scrapes ebay website for search results of the keyword found
        :param keyword: The word to be searched for on ebay
        :param quantity: The number of listings for the keyword required to be scraped.
        :return: pandas dataframe containing the listings found from the keyword search.
        """
        print(f""".....................Scraping {keyword} listings from eBay..................... 
              Please be patient as this would take some time""")
        try:
            self.__keyword = keyword
            baseurl = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.__keyword}&_sacat=0"
            self.__productlist = []
            data = []
            number_of_pages_to_scrape = math.ceil(quantity / 64)
            for page in range(1, number_of_pages_to_scrape+3):
                if page == 0 or page == 1:
                    next_page = baseurl
                else:
                    next_page = baseurl + f"&_pgn={page}"
                next_page_data = requests.get(next_page, self.__headers)
                latest_soup = BeautifulSoup(next_page_data.text, features="html.parser")
                self.__productlist.extend(latest_soup.find_all("li", {"class":"s-item"})[1:-1])

            for item in self.__productlist[1:]:
                title = item.select_one(".s-item__title").text
                link = item.select_one(".s-item__link")["href"]
                image_url = item.select_one(".s-item__image-img")['src']
                price = item.select_one(".s-item__price").text
                data.append({"title": title,"price": price, "item_url": link, "image_url": image_url, "category": keyword})
            self.__dataframe = pd.DataFrame(data)
            return self.__dataframe[:quantity]
        except ScraperError:
            raise ScraperError("System encountered a problem when scraping the site."
                               "Please ensure that you have passed in a relevant keyword and quantity")
