import unittest
from QueueStore import queuesystem

class QueuingStoreTest(unittest.TestCase):
  def setUp(self):
    self.queuesystem = queuesystem
    self.urls_list =  [
              'http://docs.python-guide.org/en/latest/writing/tests/',
              'https://www.rabbitmq.com/relocate.html',
              'https://www.youtube.com/watch?v=PIh2xe4jnpk&list=RDMMT9pNrve3ODY&index=3',
              'https://www.google.co.in/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8',
              'https://material.angularjs.org/latest/#/layout/alignment', 
              'www.google.co.in'
            ]
    self.nonurls_list = [' ', 'ab', 'http://docs.python-guide.org/e', 'http://docs.python-g', 'http://']

  def test_has_url_if_queue_empty(self):
    self.assertEqual(self.queuesystem.hasNextUrl(), False)

  def test_has_url_if_queue_not_empty(self):
    urls = ['http://docs.python-guide.org/en/latest/writing/tests/']
    self.queuesystem.storeUrlsToQueue(urls)
    self.assertEqual(self.queuesystem.hasNextUrl(), True)

    queuesystem.clearQueue()

  def test_fetch_next_url(self):
    urls = ['https://docs.python.org/2/library/queue.html']
    self.queuesystem.storeUrlsToQueue(urls)
    self.assertEqual(self.queuesystem.nextUrl(), urls[0])
    self.queuesystem.clearQueue()

