# crawler
This Project contains two directories
WebCrawler - This a module which helps to start crawl stating fromgiven url
webcrawlerdjango - This is integration of django models in DbStore and command for crawl

WebCrawler Descrition:
WebCrawler is a system where it takes url set as stating point as start crawling from on website to
other using urls extracted from the webpages of urlset

Currently My System Contain Four Parts:

UrlExtractionSystem - This system helps give a string it will validate whether it is url, can be rechable,
                      and then extract urls from the webpage and filter them to identfiy, unreduntant, relevent,
                      non duplicate url set, write now it gives back converting all of them into direct urls

QueueSystem - This System helps to queue url extracted from crawler to store and make them available to crrawler
              to when it what to extract next url
DbStore - This stores data of page into db.
UrlTackingSystem - This helps to find in which urlstate is like whether it is in queue or already crawler started
                  data extraction, or did it finish extraction of data

Wrote Tests in tests folder
run: cd WebCrawler; python -m unittest tests.<test_file_name>
eg: python -m unittest tests.urltracker

to run crawler:
cd webcrawlerdjango
python manage.py crawl <start_url>
eg: python manage.py crawl http://diply.com/and/pictures-you-wont-believe-arent-photoshopped/164239/6

Roadmap for next set of improvements.
In Extraction System we need more efficient methods to validate a url, and check for duplicate urls like for 
example http://google.com/#e == http://google.com/ which is not happening now. and identifing domain specify urls

In QueueSystem we need to improve queuing by sperating url into different queues. this helps to dfine special
crawlers for some specifc queues

Recovery System helps to recover from server crash get all urls from tracking system and enqueu them.
restarting crawler from last crashed state.

Performance improvements:
shift local queuing system to distributed queue system like rabbitmq or redis

shift urltracker which uses key value store from local to distributed

start crawlers at different server which listen to specific queues
