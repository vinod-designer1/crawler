### DBSTORE SYSTEM
#   File DbStore.py
### DESCRIPTION
#  helps to store extracted data into db
### METHODS
#   findIfUrlStoredInDb - finds if url stored inside db
#   storeUrlDataToDb - takes links, url info and stores into db
###

from abc import ABCMeta, abstractmethod
from webcrawlerdjango import models as crawlerdb

import logging
import customlogger
import threading
from Queue import Queue


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

  @abstractmethod
  def __savePageInfoToDB(self, page_info):
    pass

class DbStoreThread(threading.Thread):
    """Threaded Url Grab"""

    def __init__(self, queue, store_method, process_start, finish_task, error_report):
        threading.Thread.__init__(self)
        self.queue = queue
        self.finish_task = finish_task
        self.task_process_start = process_start
        self.task_error = error_report
        self.store_method = store_method

    def run(self):
        while True:
            # grabs host from queue
            page_info = self.queue.get()

            self.store_method(page_info)

            self.queue.task_done()

class DBStoreSystem(AbstractDBStoreSystem):

  def __init__(self):
    self._db = crawlerdb
    self._queue = Queue()
    self.__startThreads()

  def __startThreads(self):
    for i in range(2):
      t = DbStoreThread(self._queue,
             self._AbstractDBStoreSystem__savePageInfoToDB,
             self.__processStart,
             self.__finishTask,
             self.__errorReport)
      t.setDaemon(True)
      t.start()

  def __finishTask(self, message):
    pass

  def __processStart(self, message):
    pass

  def __errorReport(self, error_message=''):
    pass

  def _AbstractDBStoreSystem__savePageInfoToDB(self, page_info):
    url = page_info['url']
    body = page_info['body']
    child_urls = page_info['child_urls']

    urlstore_obj,created = self._db.URLDataStore.objects.get_or_create(url=url)

    urlrelation_store, created = self._db.URLRelationStore.objects.get_or_create(parent_url=urlstore_obj)

    for child_url in child_urls:
      temp_urlstore_obj,created = self._db.URLDataStore.objects.get_or_create(url=child_url)
      urlrelation_store.child_urls.add(temp_urlstore_obj)
    urlrelation_store.save()

    urlstore_obj.body = body.decode('utf-8', 'ignore')
    urlstore_obj.extracted = True
    urlstore_obj.save()

  #@TODO Validate data before check
  def findIfUrlStoredInDb(self, url):
    try:
      urlstore_obj = self._db.URLDataStore.objects.get(url=url)

      if urlstore_obj.extracted:
        return True
    except self._db.URLDataStore.DoesNotExist:
      stdLogger.error('No Url found in db!')

    return False

  #@TODO Validate data before insert
  def storeUrlDataToDb(self, page_info):
    if 'url' not in page_info \
       or 'body' not in page_info \
       or 'child_urls' not in page_info :
        try:
          # Raise an exception with argument
          raise ValueError("argument objects should contain url, body, child_urls keys Eg:\
            s = {'url':'', 'body':'', 'child_urls':''}, store_url_data_to_db(s) ")
        except Exception, arg:
          # Catch exception
          print 'Error: ', arg

    self._queue.put(page_info)
    

dbstore = DBStoreSystem()