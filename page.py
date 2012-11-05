import urllib, urlparse, helpers
from xml.dom.minidom import Document

class Page:
    def __init__(self, title, num, html, url, text):
        self.ID = helpers.page_hash(html)
        self.num = num
        self.title = title
        self.urls = [url]
        self.anchor_texts = [] # also contains alt text of <img>'s within <a></a>
        self.inlinks = 0.0
        self.rank = 0.0
        self.snippet = ' '.join(text.split(' ')[100:110])
        self.a = []
        self.index = 0
    
    def normalize_url(self, href, charset='utf-8'):
        # ensure that it's properly encoded
        if isinstance(href, unicode):
            href = href.encode(charset, 'ignore')
        # make absolute, relative to current page URL        
        return urlparse.urljoin(self.urls[0], href)
    
    # Public: creates an xml representation of the page
    #
    # xmldoc - an xml.dom.minidom.Document
    #
    # Returns xml element which represents page metadata
    def metadata(self, xmldoc):
        # create xml for page
        p = xmldoc.createElement("page")
        p.setAttribute("id", self.ID)
        
        # add page rank
        pagerankx = xmldoc.createElement("pagerank")
        pagerankx.appendChild(xmldoc.createTextNode(self.rank))
        p.appendChild(pagerankx)
        
        # add anchor texts
        texts = xmldoc.createElement("texts")
        p.appendChild(texts)
        for t in self.anchor_texts:
            txt = xmldoc.createElement("text")
            txt.appendChild(xmldoc.createTextNode(t))
            texts.appendChild(txt)
        
        return p
    
    def search_output(self):
        return "%s: %f\n\t%s" % (self.title, self.rank, self.snippet)