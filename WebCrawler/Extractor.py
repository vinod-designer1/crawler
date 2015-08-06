### Extraction System
#   File Extractor.py
### DESCRIPTION
#   Helps to extract urls from given url
### METHODS
#   getPageInfo - fetches url, extrac_urls and filter urls then return pagecontent object
#                   which contains pagehtml, url, extracted_urls
#   __isUrl    - check if url reachable
#   __fetchUrl - private method get html of the page
#   __extractUrls - private method extract urls from html body
#   __filterUrls - private method filter urls to get useful urls from the given urls.
###

from abc import ABCMeta, abstractmethod
import httplib, socket
from urlparse import urlparse,urljoin
import urllib2
import logging
import customlogger

# @TODO add this external dependecy in requirements installation script
from bs4 import BeautifulSoup

# Standard instance for logger with __name__
stdLogger = logging.getLogger('log')

class AbstractUrlExtractionSystem:
  __metaclass__=ABCMeta

  @abstractmethod
  def getPageInfo(self):
    pass

  @abstractmethod
  def __isUrl(self):
    pass

  @abstractmethod
  def __fetchUrl(self):
    pass

  @abstractmethod
  def __extractUrls(self):
    pass

  @abstractmethod
  def __filterUrls(self):
    pass

class UrlExtractionSystem(AbstractUrlExtractionSystem):
  DIRECT_URL = "Direct"
  PAGE_RELATIVE_URL = "Page Relative"

  def __init__(self):
    pass

  def getPageInfo(self, url):
    result = {
      'url': url,
      'body':'',
      'child_urls':[]
    }

    stdLogger.info("Started Collecting Page Info")

    if self._AbstractUrlExtractionSystem__isUrl(url):
      stdLogger.info("URL Accepted %s", url)

      pagebody, contenttype = self._AbstractUrlExtractionSystem__fetchUrl(url)
      extracted_urls = self._AbstractUrlExtractionSystem__extractUrls(pagebody, contenttype)

      stdLogger.info(extracted_urls)

      filtered_urls = self._AbstractUrlExtractionSystem__filterUrls(extracted_urls, url)

      stdLogger.info(filtered_urls)

      result['body'] = pagebody
      result['child_urls'] = filtered_urls

    return result

  def _AbstractUrlExtractionSystem__isUrl(self, url):
    parsed_url = urlparse(url)
    conn = httplib.HTTPConnection(parsed_url.netloc)
    stdLogger.info("Path %s", parsed_url.path)
    stdLogger.info("NetLoc %s", parsed_url.netloc)
    try:
        conn.request('HEAD', parsed_url.path)
        resp = conn.getresponse()
        return resp.status < 400
    except socket.gaierror:
        stdLogger.error("Host %s does not exist", url)
    except socket.error:
        stdLogger.error("Cannot connect to %s:%s.", url, 80)

    return False

  def _AbstractUrlExtractionSystem__fetchUrl(self, url):
    pagebody = ''
    contenttype = ''
    response = None

    stdLogger.info("Fetch Url Started %s", url)

    try: 
      response = urllib2.urlopen(url)

      stdLogger.info("Fetch Url Ended %s", url)
    except urllib2.HTTPError, e:
      stdLogger.error("HTTPError = " + str(e.code))
    except urllib2.URLError, e:
      stdLogger.error("URLError = " + str(e.reason))
    except httplib.HTTPException, e:
      stdLogger.error("HTTPException")
    except Exception:
      import traceback
      stdLogger.error("generic exception: " + traceback.format_exc())

    if response:
      stdLogger.info("Status code %s", response.getcode())
      pagebody = response.read()
      stdLogger.info("Read Url Ended %s", url)
      contenttype = response.info().getheader('Content-Type')
      stdLogger.info("Url Contettype Ended %s", url)
      response.close()

    stdLogger.info("Extracted body with conten type %s for url %s", contenttype, url)

    return pagebody, contenttype

  def __getUrlsFromHtml(self, htmlbody):
    soup_obj = BeautifulSoup(htmlbody)
    soup_obj.prettify()

    urls = []

    stdLogger.info("Getting url from html started")

    for anchor_tag in soup_obj.find_all('a'):
      url = anchor_tag.get('href')

      stdLogger.info("Extracted url %s", url)

      if url:
        urls.append(url)

    return urls

  def _AbstractUrlExtractionSystem__extractUrls(self, pagebody, contenttype):
    extracted_urls = []

    stdLogger.info("Extracting url system started")

    if 'text/html' in contenttype:
      extracted_urls = self.__getUrlsFromHtml(pagebody)

    stdLogger.info("Extracting url system ended")

    return extracted_urls

  # @TODO fix to find relative url
  def __getTypeOfUrl(self, url):    

    if bool(urlparse(url).netloc):
      return self.DIRECT_URL

    return self.PAGE_RELATIVE_URL

  # @TODO improve filtering urls
  def _AbstractUrlExtractionSystem__filterUrls(self, urls, root_url):
    filtered_urls = []

    for url in urls:
      url_type = self.__getTypeOfUrl(url)
      
      if url_type == self.DIRECT_URL:
        url = url
      elif url_type == self.PAGE_RELATIVE_URL:
        url = urljoin(root_url, url)

      filtered_urls.append(url)

    return filtered_urls