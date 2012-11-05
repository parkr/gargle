#! /usr/bin/env python

import argparse
from searchr import Searchr
from brain import Brain

if __name__ == "__main__":
    # consider command-line options
    # => --test-data url_file.txt
    parser = argparse.ArgumentParser(prog='gargle.py', description='An implementation of a web crawler, Gargle.')
    parser.add_argument('-u', '--urls', nargs=1, default='./test/test3.txt', metavar='bar.txt', help='user-defined doc of newline-delimited urls')
    parser.add_argument('-q', '--query', nargs=argparse.REMAINDER, metavar='query string', help='query for the single-run test, will not prompt. THIS MUST BE THE LAST ARGUMENT')
    args = parser.parse_args()
    
    # normalize values of test_data
    user_defined_url_doc = ''
    if type(args.urls) is str:
        user_defined_url_doc = args.urls.strip()
    elif type(args.urls) is list:
        user_defined_url_doc = args.urls[0].strip()
    else:
        user_defined_url_doc = None
        
    user_defined_query = ''
    if type(args.query) is str:
        user_defined_query = args.query.strip()
    elif type(args.query) is list:
        user_defined_query = " ".join(args.query)
    else:
        user_defined_query = None
        
    brain = Brain()
    brain.parse_urls(user_defined_url_doc)
    brain.process_pages()
    brain.calc_page_ranks()
    brain.write_metadata()
    
    searchr = Searchr(brain)
    searchr.build_index()
    if user_defined_query == None:
        # read in queries and output results from LSI
        try:
            query = raw_input('Enter a query: ')
        except KeyboardInterrupt:
            query = ""
        while query != "":
            try:
                # process query
                print "Showing results for '%s':" % query
                print searchr.process_query(query)
                # get new query
                query = raw_input('Enter a query: ')
            except KeyboardInterrupt:
                query = ""
    else:
        # process based on input query
        print "Showing results for '%s':" % user_defined_query
        print searchr.process_query(user_defined_query)
