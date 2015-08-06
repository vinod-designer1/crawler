import unittest
from Extractor import UrlExtractionSystem
import urllib2

#@TODO need to get more data to test extracted urls set, filterUrls, and getPageInfo
class ExtractorTest(unittest.TestCase):
  def setUp(self):
    self.url_extraction_system = UrlExtractionSystem()
    self.urls_list =  [
              ['http://docs.python-guide.org/en/latest/writing/tests/', 'text/html'],
              ['https://www.rabbitmq.com/relocate.html', 'text/html'],
              ['https://www.youtube.com/watch?v=PIh2xe4jnpk&list=RDMMT9pNrve3ODY&index=3','text/html'],
              ['https://www.google.co.in/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8', 'text/html'],
              ['https://material.angularjs.org/latest/#/layout/alignment', 'text/html'], 
              ['www.google.co.in', 'text/html']
            ]

    self.nonurls_list = [' ', 'ab', 'http://docs.python-guide.org/e', 'http://docs.python-g', 'http://']

  def test_is_url_in_urls(self):
    for url in self.urls_list:
      is_url = self.url_extraction_system._AbstractUrlExtractionSystem__isUrl(url[0])
      self.assertEqual(is_url, True)

  def test_is_url_in_non_urls(self):
    for url in self.nonurls_list:
      is_url = self.url_extraction_system._AbstractUrlExtractionSystem__isUrl(url[0])
      self.assertEqual(is_url, False)

  def checkEqualList(self, L1, L2):
    return len(L1) == len(L2) and sorted(L1) == sorted(L2)

  def test_fetch_url_for_all_urls(self):
    for url in self.urls_list:
      pagebody, contenttype = self.url_extraction_system._AbstractUrlExtractionSystem__fetchUrl(url[0])
      self.assertEqual(url[1] in contenttype, True)

    for url in self.nonurls_list:
      pagebody, contenttype = self.url_extraction_system._AbstractUrlExtractionSystem__fetchUrl(url)
      self.assertEqual(pagebody, '')
      self.assertEqual(contenttype, '')

