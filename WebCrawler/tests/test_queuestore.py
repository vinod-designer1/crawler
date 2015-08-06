import unittest
from QueueStore import queuesystem

class QueuingStoreTest(unittest.TestCase):
  def test_has_url_if_queue_empty(self):
    self.assertEqual(queuesystem.hasNextUrl(), False)

  def test_has_url_if_queue_not_empty(self):
    urls = ['http://docs.python-guide.org/en/latest/writing/tests/']
    queuesystem.storeUrlsToQueue(urls)
    self.assertEqual(queuesystem.hasNextUrl(), True)

    queuesystem.clearQueue()

  def test_fetch_next_url(self):
    urls = ['https://docs.python.org/2/library/queue.html']
    queuesystem.storeUrlsToQueue(urls)
    self.assertEqual(queuesystem.nextUrl(), urls[0])
    queuesystem.clearQueue()

