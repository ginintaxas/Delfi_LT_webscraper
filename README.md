# delfi lt web scraper

## Description
A Python-based web scraper that extracts top page articles from www.delfi.lt. It fetches and parses web pages, then saves the data in txt/csv/Sqlite format.

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

*Note whilst selecting output file don't forget to add file format extension (.txt, .csv)*

### Subdirectory Options by Language
- **Lithuanian (`lt`)**: `tv`, `laisvalaikis`, `verslas`, `sportas`, `veidai`
- **English (`en`)**: `politics`, `business`, `world-lithuanians`, `expats-in-lt`, `culture`, `lifestyle`
- **Russian (`ru`)**: `poslednie`, `news/economy`, `detektor-lzhi`, `sport`, `misc`
### Subdirectory Options by format
- **sqlite**: articles are stored in a database called articles
- **txt**: articles are stored in a plain text file
- **csv**: articles are stored in csv
- **txt_full**: articles are stored in format - title is the same as file name and the contents of the full article are stored in the text file
  
  *txt_full option can only be used with a directory as an output file because this option generates more than one file*
### Example config file
```bash
{
  "subdir": "culture",
  "language": "en",
  "output": {
    "format": "sqlite",
    "file": "output/articles.db"
  }
}
