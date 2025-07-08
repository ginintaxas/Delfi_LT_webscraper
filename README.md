# delfi_scrapper

## Description
A Python-based web scraper that extracts top page articles from www.delfi.lt. It fetches and parses web pages, then saves the data in CSV/Sqlite format.

## Table of Contents
- [Installation](#installation)
- [Description](#description)
- [Usage](#usage)
- [Config](#config)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-scraper.git
2. Install requirements:
   ```bash
   cd /install/dir
   pip install -r requirements.txt

## Description
A Python-based web scraper that extracts data from www.delfi.lt using BeautifulSoup and Selenium for JS generated content.  
All configuration (subdirs to scrape, language) is managed through a JSON config file for easy customization.

## Usage
Basic usage:
```bash
python scrapper.py
```

## Config
All configuration is done through the config.json file which is located in the same github repo with everything else.
Everything is mostly self explanatory, language selects language that delfi provides (lt, ru or en), subdir so (culture, sports and so on) and the output format.
**Note whilst selecting output format don't forget to add file format extension (.txt, .csv)**
Config options are listed here:
