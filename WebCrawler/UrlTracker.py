### Tracking System
#   File UrlTracker.py
### DESCRIPTION
#   helps to track url state to check whether url extracted or not
#   there are 4 states for url 
#   1 - in queue, 2 - received by crawler, 3 - in process, 4 - done processing
### METHODS
#   isUrlInQueue - returns boolean tells url in queue
#   removeUrlFromQueue - removes url from queue
#   getUrlState - returns current state for url in process
#   setUrlState - helps setting url state
###

from abc import ABCMeta, abstractmethod
import logging
import customlogger

# Standard instance for logger with __name__
stdLogger = logging.getLogger('log')

class AbstractUrlTracker:
  __metaclass__=ABCMeta

  @abstractmethod
  def isUrlInQueue(self, url):
    pass

  @abstractmethod
  def getUrlState(self, url):
    pass

  @abstractmethod
  def removeUrlFromQueue(self, url):
    pass

  @abstractmethod
  def setUrlState(self, url, state):
    pass

class UrlTrackingSystem(AbstractUrlTracker):
  IN_QUEUE = 1
  IN_CRAWLER = 2
  IN_PROGRESS = 3
  DONE_PROCESS = 4
  NO_URL = -1

  def __init__(self):
    self._trackingstore = {}

  def isUrlInQueue(self, url):
    if url in self._trackingstore:
      if self._trackingstore[url] == self.IN_QUEUE:
        return True
    return False

  def removeUrlFromQueue(self, url):
    self._trackingstore.pop(url, None)

  def getUrlState(self, url):
    if url in self._trackingstore:
      return self._trackingstore[url]
    return self.NO_URL

  def setUrlState(self, url, state):
    self._trackingstore[url] = state

urltracker = UrlTrackingSystem()
