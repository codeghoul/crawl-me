from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:
    project_name = ''
    base_url = ''
    domain_name = ''
    queued_file = ''
    crawled_file = ''
    queued = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = 'projects/' + project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queued_file = Spider.project_name + '/queued.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First Spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queued = file_to_set(Spider.queued_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' crawling ' + page_url)
            print('Queued: ' + str(len(Spider.queued)) + ' | Crawled: ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queued.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html; charset=utf-8':
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print('Error : Cannot crawl page.')
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for link in links:
            if link in Spider.queued:
                continue
            if link in Spider.crawled:
                continue
            if Spider.domain_name not in link:
                continue
            Spider.queued.add(link)

    @staticmethod
    def update_files():
        set_to_file(Spider.queued, Spider.queued_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
