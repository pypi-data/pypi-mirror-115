### Youtube Comment Extractor
This package scrapes comments from any Youtube video links. The comments will be further analysed and used for sentiment analysis.

The package returns a pandas dataframe.

### Installation
The package can be installed via PYPI and requires python3

``` shell 
$ pip install git+https://github.com/linda-oranya/YT_comments_scrapper.git
```

``` shell 
$ pip install YT-comments-scrapper
```

Usage
This libary can be used when the key interest is to retrieve comments from a YouTube link. The packages uses selenium since YouTube pages are mainly JavaScript rendered.

That means you have to add the path to your chromedriver. Pls install here : https://sites.google.com/chromium.org/driver/, if you don't have installed.

The package allows you to input video link, the range of comments you want to scrape and path to your chromedriver. 

Leave the chrome tab open when extracting the comments.

Sample codes

``` shell 
from yt_scrapper import YtScrapper

scrapper = YtScrapper("<Youtube link>",<num_of_comments>,"<path_to_chromedriver>")

scrapper.scrape_comments()
```

### Development
You can contribute to this project by cloning this repo and pushing to a branch for review and merging.

Or

 Create an issue with the issue link: https://github.com/linda-oranya/YT_comments_scrapper/issues

 ## License

MIT

**It is a Free Software**

