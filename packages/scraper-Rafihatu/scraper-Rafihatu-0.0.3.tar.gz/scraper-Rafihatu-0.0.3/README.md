# eBay Web Scraper

## Description
This is a web scraper that extracts info about listings from popular e-commerce site, eBay. 
Collects info about the category the listing belongs to, title of listing, link to the listing, link to the listing's image and price of each listing.

## Technologies

* [Python 3.9](https://python.org) : Base programming language for development. The latest version of python.
* [Docker Engine and Docker Compose](https://www.docker.com/) : Containerization of the application and services orchestration
* [Postgres Database](https://www.postgresql.org) : Database where scraped listings are stored.


## Getting Started

Using this scraper is very simple, all you need is to have Git and Docker Engine installed on your machine. 
If you do not wish to use docker, simply create your own virtual environment and run `pip install -r requirements.txt` from the root directory to
install the requirements stated in the `requirements.txt` file
Don't forget to add your postgres database connection variables in the `.env` file in the root folder.
Example of what the `.env` file should look like
```
DB_PORT = XXXX
DB_HOST = your_database_host
DB_USER = your_username
DB_NAME = the_name_of_your_database_here
DB_PASSWORD = your_password_here

```


The scraper can be found in src/scraper
eBay contains 3 methods which are `scrape()`, `add_category_to_database()`, `add_listing_to_database()`. 
The methods are self-explanatory. 
scrape takes in the category/keyword, and the number/quantity of listings to be scraped while `add_category_to_database()` and `add_listing_to_database()` adds categories and listings to their 
respective databases.

Example:
```
    from src.scraper import eBay
    ebay = eBay()
    ebay.scrape(keyword="book", quantity=200)
    ebay.add_category_to_database()
    ebay.add_listings_to_database()
```

## Testing


This project has pytest embedded in it and can be run with the following command `python -m pytest tests/` from the root directory.
Note: This should be run after after all necessary database connection variables have been declared in the.env file


## License

The MIT License - Copyright (c) 2021 - Rafihatu Bello
