### DBSTORE SYSTEM
#   File DbStore.py
### DESCRIPTION
#  helps to store extracted data into db
### METHODS
#   findIfUrlStoredInDb - finds if url stored inside db
#   storeUrlDataToDb - takes links, url info and stores into db
###

from abc import ABCMeta, abstractmethod
import logging
import customlogger

# Standard instance for logger with __name__
stdLogger = logging.getLogger('log')

class AbstractDBStoreSystem:
  __metaclass__=ABCMeta

  @abstractmethod
  def findIfUrlStoredInDb(self, url):
    pass

  @abstractmethod
  def storeUrlDataToDb(self, urls):
    pass

class DBStoreSystem(AbstractDBStoreSystem):

  def __init__(self):
    self.db = None

  def findIfUrlStoredInDb(self, url):
    return False

  def storeUrlDataToDb(self, urls):
    pass

dbstore = DBStoreSystem()