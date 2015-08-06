### QUEUING System
#   File QueueStore.py
### DESCRIPTION
#   helps to queue urls extracted by crawlers extractin system
### METHODS
#   hasNextUrl -  to check whether the queue is empty or not
#   nextUrl - This method helps to get next item in queue
#   storeUrlsToQueue - This methods takes the links a added in to queues 
###

from abc import ABCMeta, abstractmethod
from Queue import Queue
from UrlTracker import urltracker


class AbstractQueueSystem:
  __metaclass__=ABCMeta

  @abstractmethod
  def hasNextUrl(self):
    pass

  @abstractmethod
  def nextUrl(self):
    pass

  @abstractmethod
  def storeUrlsToQueue(self, urls):
    pass

class QueueSystem(AbstractQueueSystem):
  def __init__(self):
    self._queue = Queue()
    self._urltracker = urltracker

  def hasNextUrl(self):
    return not self._queue.empty()

  def clearQueue(self):
    with self._queue.mutex:
      self._queue.queue.clear()

  def nextUrl(self):
    if not self._queue.empty():
      return self._queue.get()
    return ''

  def storeUrlsToQueue(self, urls):
    for url in urls:
      if not self._urltracker.isUrlInQueue(url):
        self._queue.put(url)

        self._urltracker.setUrlState(url, self._urltracker.IN_QUEUE)

queuesystem = QueueSystem()