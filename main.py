import argparse
from scraper import scrape_data

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
                                     'This script allows the user to enter a search term for Bing Images '
                                     'and annotate the images returned by the search request.')
    parser.add_argument('search_term', help='the specific phrase that the user wants to search')

    args = parser.parse_args()

    correct_search_term = input('Are you sure you want to search for \'' + args.search_term + '\'? [Y/n]:')

    if correct_search_term == 'Y':
        scrape_data(args.search_term)