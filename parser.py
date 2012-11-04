from bs4 import BeautifulSoup
from xml.dom.minidom import Document
from datetime import datetime
from page import Page
import urllib2

class Parser:
    
    def __init__(self):
        self.urls = []
        self.pages = []
        self.pages_with_ids = {}
        self.backup_pages_dir_rel_path = "./test3"
        
    def __get_html(self, num, url):
        encoding = False
        try:
            f = open("%s/%s.html" % (self.backup_pages_dir_rel_path, num), 'r')
        except IOError:
            return None
            try:
                f = open("%s/%s.htm" % (self.backup_pages_dir_rel_path, num), 'r')
                encoding = "iso-8859-1"
            except IOError:
                return None
        
        html = f.read()
        try:
            unicode_html = unicode(html, 'utf-8')
        except UnicodeDecodeError:
            unicode_html = unicode(html, 'windows-1252')
            if encoding:
                unicode_html = unicode(html, encoding)
            else:
                unicode_html = unicode(html, 'windows-1252')
        return unicode_html
    
    def parse_urls(self, filename='./test/test3.txt'):
        # reads in URLs & normalizes
        f = open(filename, 'r')
        for line in f.readlines():
            els = line.strip().split(',')
            self.urls.append( (els[0], els[1]) )
    
    def process_pages(self):
        skipped = []
        for (num, url) in self.urls:
            if not (num and url):
                skipped.append(num)
                continue
            
            print "Processing URL (%s): %s" % (num, url)
            html = self.__get_html(num, url)
            if html is None:
                skipped.append(num)
                continue
            
            soup = BeautifulSoup(html.encode('utf-8', 'ignore'), "lxml")
            page = Page(title=soup.title.string, html=soup.prettify(), soup=soup)
            self.pages_with_ids[page.ID] = page
            
            for link in soup.find_all('a'):
                
                link.get('href')
            
            self.pages.append(page)
        print len(self.pages)
        return None
        print "Skipped page(s) %s because of an error." % (', '.join(skipped))
    
    def write_metadata(self):
        # write metadata.xml
        doc = Document()
        doc.appendChild(doc.createElement("date").appendChild(doc.createTextNode(datetime.now().isoformat())))
        pagesx = doc.createElement("pages")
        doc.appendChild(pagesx)
        for p in self.pages:
            pagesx.appendChild(p.metadata(doc))