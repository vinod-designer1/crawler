### FILE
# Crawler.py
### DESCRIPTION
# This class helps run a webcrawler which has four basic components
#   Extraction System - This system helps extract data from url and extract useful information about url
#                       in our case extract links, and url filtration system to filter the urls extracted.
#   QueueStore System - This helps to queue links that are extracted from extraction system to give to crawlers.
#                       in our case this class help get next link, store_url_to_queue methods.
#   DBStore System    - This helps store content to db and extract from db
#                     - in our case this class helps to find_if_url_stored_in_db, store_urls_to_db.
#   Tracking System   - This helps to tracking url state in the process once queued into queues, 
#                       in our case to know whether url is extracted or got stuck somewhere. 
#                       helps in failures of servers
###

from Extractor import UrlExtractionSystem
from QueueStore import queuesystem
from DbStore import dbstore
from UrlTracker import urltracker, UrlTrackingSystem
import logging
import customlogger

# Standard instance for logger with __name__
stdLogger = logging.getLogger('log')

class Crawler():
  def __init__(self):
    self.queuesystem = queuesystem
    self.dbstore = dbstore
    self.urltracker = urltracker
    self.extractor = UrlExtractionSystem()

  def startcrawler(self, urls):
    self.queuesystem.storeUrlsToQueue(urls)

    while True:
      
      if self.queuesystem.hasNextUrl():
        url = self.queuesystem.nextUrl()

        if url.strip() != '':
          self.urltracker.setUrlState(url, self.urltracker.IN_CRAWLER)

          if not self.dbstore.findIfUrlStoredInDb(url):
            self.urltracker.setUrlState(url, self.urltracker.IN_PROGRESS)

            stdLogger.info('Extraction Started!')
            page_info = self.extractor.getPageInfo(url)
            stdLogger.info('Done Extraction!')

            stdLogger.info('Queuing Started!')
            self.queuesystem.storeUrlsToQueue(page_info['child_urls'])
            stdLogger.info('Queuing Ended!')

            stdLogger.info('DBStore Started!')
            self.dbstore.storeUrlDataToDb(page_info)
            stdLogger.info('DBStore Ended!')

          self.urltracker.setUrlState(url, self.urltracker.DONE_PROCESS)

          stdLogger.info(self.urltracker._trackingstore)
        else:
          self.urltracker.setUrlState(url, self.urltracker.NO_URL)
      else:
        self.urltracker.setUrlState(url, self.urltracker.NO_URL)


start_urls = ['http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#findAllNext(name, attrs, text, limit, **kwargs) and findNext(name, attrs, text, **kwargs)']
crawler = Crawler()
crawler.startcrawler(start_urls)
