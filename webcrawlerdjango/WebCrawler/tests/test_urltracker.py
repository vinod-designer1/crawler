import unittest
from UrlTracker import urltracker

class UrlTrackerTest(unittest.TestCase):
  def setUp(self):
    self.url_tracker = urltracker
    self.urls_list =  [
              'http://docs.python-guide.org/en/latest/writing/tests/',
              'https://www.rabbitmq.com/relocate.html',
              'https://www.youtube.com/watch?v=PIh2xe4jnpk&list=RDMMT9pNrve3ODY&index=3',
              'https://www.google.co.in/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8',
              'https://material.angularjs.org/latest/#/layout/alignment', 
              'www.google.co.in'
            ]
    self.nonurls_list = [' ', 'ab', 'http://docs.python-guide.org/e', 'http://docs.python-g', 'http://']

  def test_is_url_in_queue(self):
    for url in self.urls_list:
      self.url_tracker.setUrlState(url, self.url_tracker.IN_QUEUE)
      is_url_in_queue = self.url_tracker.isUrlInQueue(url)

      self.assertEqual(is_url_in_queue, True)

      self.url_tracker.removeUrlFromQueue(url)

  def test_is_url_not_in_queue(self):
    for url in self.urls_list:
      is_url_in_queue = self.url_tracker.isUrlInQueue(url)

      self.assertEqual(is_url_in_queue, False)

  def test_if_i_get_correct_state(self):
    for url in self.urls_list:
      self.url_tracker.setUrlState(url, self.url_tracker.IN_QUEUE)
      url_state = self.url_tracker.getUrlState(url)

      self.assertEqual(url_state, self.url_tracker.IN_QUEUE)

      self.url_tracker.removeUrlFromQueue(url)

    for url in self.urls_list:
      url_state = self.url_tracker.getUrlState(url)

      self.assertEqual(url_state, self.url_tracker.NO_URL)

      self.url_tracker.removeUrlFromQueue(url)



    
