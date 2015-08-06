# import unittest
from DbStore import dbstore

class DbStoreTest(unittest.TestCase):
  def setUp(self):
    self.dbstore = dbstore
    self.urls_list =  [
              ['http://docs.python-guide.org/en/latest/writing/tests/', 'text/html'],
              ['https://www.rabbitmq.com/relocate.html', 'text/html'],
              ['https://www.youtube.com/watch?v=PIh2xe4jnpk&list=RDMMT9pNrve3ODY&index=3','text/html']
            ]

    self.nonurls_list = [' ', 'ab', 'http://docs.python-guide.org/e', 'http://docs.python-g', 'http://']
    self.non_page_info_test_data = [{
       'url': ''
      },{
       'url': '',
       'page_info':'',
      },
      {
       'url': '',
       'body':'',
       'child_urls':[]
      },
      {
       'url': '',
       'body':[],
       'child_urls':''
      },{
       'url': [],
       'body':'',
       'child_urls':[]
      },
      {
       'url': 'https://www.rabbitmq.com/relocate.html',
       'body':'',
       'child_urls':[]
      },
      {
       'url': 'https://www.rabbitmq.com/relocate.html',
       'body':'fferferf',
       'child_urls':['frfrfr', 'frfrrv']
      },
      {
       'url': 'https://www.rabbitmq.com/relocate.html',
       'body':'fferferf',
       'child_urls':['http://docs.python-guide.org/en/latest/writing/tests/']
      }
    ]
    self.page_info_test_data = [
      {
       'url': 'https://www.rabbitmq.com/relocate.html',
       'body':'<html><head></head><body>Hello!</body></html>',
       'child_urls':['http://docs.python-guide.org/en/latest/writing/tests/']
      }
    ]

  def test_find_if_url_stored_not_extracted(self):
    for url in self.urls_list:
      is_url_extracted = self.dbstore.findIfUrlStoredInDb(url)

      self.assertEqual(is_url_extracted, False)

  def test_find_if_url_stored_extracted(self):
    for url in self.urls_list:
      page_info = {
        'url': url,
        'body':'Hello!',
        'child_urls':['http://docs.python-guide.org/en/latest/writing/tests']
      }
      self.dbstore._AbstractDBStoreSystem__savePageInfoToDB(page_info)
      is_url_extracted = self.dbstore.findIfUrlStoredInDb(url)

      self.assertEqual(is_url_extracted, True)

  def test_store_url_data_to_db(self):
    for page_info in self.non_page_info_test_data:
      self.dbstore._AbstractDBStoreSystem__savePageInfoToDB(page_info)

    for page_info in self.page_info_test_data:
      self.dbstore._AbstractDBStoreSystem__savePageInfoToDB(page_info)