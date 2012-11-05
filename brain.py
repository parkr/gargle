from bs4 import BeautifulSoup
from xml.dom.minidom import Document
from page import Page
from progressbar import *
import urllib2, helpers, numpy, datetime

class Brain:
    
    # Public: Initializes a new instance of Brain and sets up instance variables
    #
    # Returns nothing
    def __init__(self):
        self.S = []
        self.urls = []
        self.pages = []
        self.pages_with_ids = {}
        self.urls_with_nums = {}
        self.indices_with_pages = {}
        self.adj = None
        self.ranks = None
    
    # Public: reads in the URLs from the file
    #
    # filename - the filename of the file with the newline-delimited
    #            (num,url) comma-separated values
    #
    # Returns nothing
    def parse_urls(self, filename='./test/test3.txt'):
        # reads in URLs & normalizes
        f = open(filename, 'r')
        for line in f.readlines():
            els = line.strip().split(',')
            self.urls.append( (els[0], els[1]) )
            self.S.append(els[1])
    
    # Public: Grabs the HTML and creates the instances of Page for each URL
    #
    # Returns nothing
    def process_pages(self):
        skipped = []
        pbar = ProgressBar(widgets=['Processing pages: ', SimpleProgress()], maxval=len(self.urls)).start()
        i = 0
        
        for (num, url) in self.urls:
            pbar.update(int(num))
            if (num and url):
                html = helpers.get_html(num, url)
                if html is not None:
                    self.urls_with_nums[url] = num
                    soup = BeautifulSoup(html.encode('utf-8', 'ignore'), 'lxml')
                    page = Page(title=soup.title.string, num=num, html=soup.prettify(), url=url, text=soup.body.get_text())
                    page.index = i
                    self.indices_with_pages[i] = page
                    if page.ID not in self.pages_with_ids.keys():
                        self.pages_with_ids[page.ID] = page
                    else:
                        raise RuntimeError('COLLISION: %s collides with %s with hash %s.' % (page.num, self.pages_with_ids[page.ID].num, page.ID))
                    for link in soup.find_all('a'):
                        if link.get('href') and 'mailto:' != link.get('href').strip()[0:7]:
                            page.a.append(link)
                    self.pages.append(page)
                    i += 1
                else:
                    skipped.append(num)
            else:
                skipped.append(num)
        pbar.finish()
        print "Skipped page(s) %s because of an error." % (', '.join(skipped))
    
    # Public: Calculates the PageRank value for all the pages
    #
    # Returns nothing
    def calc_page_ranks(self, d=0.85):
        self.adj = numpy.zeros( (len(self.pages_with_ids),len(self.pages_with_ids)) )
        pbar = ProgressBar(widgets=['Processing links: ', SimpleProgress()], maxval=len(self.pages_with_ids.keys())).start()
        progress = 1
        for (ID, page) in self.pages_with_ids.iteritems():
            pbar.update(progress)
            # magic PageRank
            for a in page.a:
                href = a.get('href')
                # normalize URLS
                url = page.normalize_url(href)
                if url in self.S:
                    soup = BeautifulSoup(helpers.get_html(self.urls_with_nums[url]).encode('utf-8', 'ignore'), 'lxml')
                    ID = helpers.page_hash(soup.prettify())
                    if ID in self.pages_with_ids.keys():
                        #print "%s (#%d) cites %s (#%d)" % (page.num, page.index, self.pages_with_ids[ID].num, self.pages_with_ids[ID].index)
                        #print self.urls[int(self.pages_with_ids[ID].num)-1]
                        self.adj[page.index][self.pages_with_ids[ID].index] = 1.0
            progress += 1
        # Normalize adjacency matrix into PageRanks
        pbar = ProgressBar(widgets=['Normalizing adjacencies: ', SimpleProgress()], maxval=len(self.pages_with_ids.keys())).start()
        progress = 1
        col_sums = numpy.sum(self.adj, axis=1)
        for (ID, page) in self.pages_with_ids.iteritems():
            pbar.update(progress)
            for k in xrange(len(self.adj[page.index])):
                if col_sums[page.index] != 0:
                    self.adj[page.index][k] = self.adj[page.index][k] / col_sums[page.index]
                else:
                    self.adj[page.index][k] = 0.0
                self.indices_with_pages[k]
            progress += 1  
        pbar.finish()
        numpy.savetxt("adj.txt", self.adj)
        # Run PageRank and converge to principal eigenvector of adj matrix
        self.ranks = numpy.ones(len(self.pages_with_ids.keys()))
        z = numpy.ones(len(self.pages_with_ids.keys()))
        b = 1.0 - d
        pbar = ProgressBar(widgets=['Running PageRank: ', SimpleProgress()], maxval=1000).start()
        for m in xrange(1000):
            pbar.update(m)
            u = numpy.dot(self.adj, self.ranks)
            e = d*u
            f = b*z
            self.ranks = e+f
        pbar.finish()
        # Updating ranks of the pages
        pbar = ProgressBar(widgets=['Updating pages with new ranks: ', SimpleProgress()], maxval=len(self.pages_with_ids.keys())).start()
        progress = 1
        for (ID, page) in self.pages_with_ids.iteritems():
            pbar.update(progress)
            page.rank = self.ranks[page.index]
            progress += 1
        pbar.finish()
        numpy.savetxt("page_ranks.txt", self.ranks)
    
    # Public: Writes the page metadata to metadata.xml
    #
    # Returns nothing
    def write_metadata(self):
        # write metadata.xml
        doc = Document()
        index = doc.createElement("index")
        doc.createElement(index)
        # input the date
        datex = doc.createElement("date")
        date = doc.createTextNode(datetime.datetime.now().isoformat())
        datex.appendChild(date)
        index.appendChild(datex)
        # add pages
        pagesx = doc.createElement("pages")
        index.appendChild(pagesx)
        for (ID, p) in self.pages_with_ids.iteritems():
            pagesx.appendChild(p.metadata(doc))
        with open('metadata.xml', 'w') as f:
            f.write(doc.toprettyxml(indent='  '))
