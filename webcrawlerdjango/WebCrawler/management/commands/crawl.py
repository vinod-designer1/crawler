from django.core.management.base import BaseCommand, CommandError
from WebCrawler.Crawler import Crawler
class Command(BaseCommand):
  help = 'fetch articles from hackernews'

  def add_arguments(self, parser):
    parser.add_argument('start_url')

  def handle(self, *args, **options):

    start_url = args[0]

    self.stdout.write(start_url)


    start_urls = [start_url]
    crawler = Crawler()
    
    self.stdout.write('Crawling started')
    crawler.startcrawler(start_urls)