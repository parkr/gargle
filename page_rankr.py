import numpy

class PageRankr:
    def __init__(self, d=0.85, size=(0,0)):
        self.__d = d
        self.__m = numpy.zeros(size)
        self.__pages = []
    
    def add_page(self, page):
        self.__pages.append(page)
    
    def calc_page_ranks(self):
        raise RuntimeError('PageRankr#calc_page_ranks has not been implemented yet.')
        # re-create self.__m
        