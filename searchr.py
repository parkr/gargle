from progressbar import ProgressBar, SimpleProgress
from operator import itemgetter
from brain import Brain

class Searchr:
    
    # Public: Initializes a new instance of Searchr and sets up instance variables
    #
    # brain - an instance of Brain which contains pages with caluclated PageRank values
    #
    # Returns nothing
    def __init__(self, brain=Brain()):
        self.brain = brain
        self.anchor_text_with_ranks_with_pages = {}
    
    # Public: Create index based on the ranks in the brain
    #
    # Returns nothing
    def build_index(self):
        pbar = ProgressBar(widgets=['Processing pages: ', SimpleProgress()], maxval=len(self.brain.pages_with_ids.keys())).start()
        index = 1
        for (ID, page) in self.brain.pages_with_ids.iteritems():
            pbar.update(index)
            for a in page.a:
                anchor_text = a.get_text()
                if anchor_text in self.anchor_text_with_ranks_with_pages.keys():
                    self.anchor_text_with_ranks_with_pages[anchor_text].append((page.rank, page))
                else:
                    self.anchor_text_with_ranks_with_pages[anchor_text] = [(page.rank, page)]
            index += 1
        pbar.finish()
    
    # Public: Process query string and print output
    #
    # query - a string containing a query
    #
    # Returns nothing
    def process_query(self, query):
        results = []
        already_collected = []
        for anchor_text in self.anchor_text_with_ranks_with_pages.keys():
            if query in anchor_text:
                for pages in self.anchor_text_with_ranks_with_pages[anchor_text]:
                    if pages[1].ID not in already_collected:
                        results.append(pages)
                        already_collected.append(pages[1].ID)
        result_rank = 1
        for (rank, page) in sorted(results, key=itemgetter(0)):
            print "%d. %s" % (result_rank, page.search_output())
