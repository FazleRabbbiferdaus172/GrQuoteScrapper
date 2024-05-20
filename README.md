# Quote scraping & API

This project Scrape quotes from Goodreads. Extracts the quoted text, author name, and any additional relevant information on SQLlite database. Then exposes api to crud on then.

# Architecture

`scrapy` is used for scraping `scrapy`.

Schemas/models representing quotes, author and tag are implemented using `pydantic` & `sqlAlchemy`, so they have parsing&validation
out-of-the-box.

As `FastAPI` has first-class support for pydantic and has openapi docs viewer, it was the perfect fit for the project.

Sadly because of time constrains `SQLite` was used for db technology. (Will add support for other relational db)

## Installation

1. Install python 3.10
2. clone the repo
3. create a virtual environment `python -m venv venv`
4. activate virtual environment `source venv/bin/activate`
5. install the requirements `pip install -r requirements.txt`

## Running
In the same terminal window make sure the virtual environment is active
1. Change directory: `cd ./quotes_scraper`
2. Now in terminal window, Run Scrapper: `scrapy crawl quotespider`
3. Open another terminal window.
4. activate virtual environment in the new terminal `source venv/bin/activate`
5. if not in 'quotes_scrapper' directory change the directory.
6. Now in terminal window, Run fastapi: `fastapi run`

# Docs
After runninfg fastapi, OpenApi docs should be available at http://localhost:8000/docs