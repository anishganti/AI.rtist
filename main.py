import argparse
from scraper import scrape_data

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # parse command line arguments
    # should contain help flag and/or search term
    parser = argparse.ArgumentParser(description=
                                     'This script allows the user to enter a search term for Bing Images '
                                     'and annotate the images returned by the search request.')
    parser.add_argument('search_term', help='the specific phrase that the user wants to search')

    args = parser.parse_args()
    print(args.search_term)

    # prompt user if they are sure they want to search for entered term
    correct_search_term = input('Are you sure you want to search for \'' + args.search_term + '\'? [Y/n]:')

    # if the user enters yes then call the web scraper
    if(correct_search_term == 'Y'):
        scrape_data(args.search_term)
