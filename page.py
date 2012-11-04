import hashlib, StringIO, codecs
from xml.dom.minidom import Document

class Page:
    def __init__(self, title, num, html):
        self.ID = self.id_hash(html)
        self.num = num
        self.title = title
        self.urls = []
        self.anchor_texts = [] # also contains alt text of <img>'s within <a></a>
        self.rank = 0.0
        self.snippet = ' '.join(html.split()[:10])
        self.a = []
    
    # Public: creates a hash based on the HTML.
    #
    # Returns the md5 hash of the HTML
    def id_hash(self, html):
        return hashlib.md5(html.encode(errors='ignore')).hexdigest()
    
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
        return "%s: %f\n%s" % (self.title, self.rank, self.snippet)