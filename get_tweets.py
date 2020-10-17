#!/usr/bin/env python3

from twitter_search_service import TwitterSearchService
import asyncio
import jsonpickle
import sys
import getopt

def write_file(filename, data):
    f = open(filename, 'w+')
    f.writelines(data)
    f.close()

async def main_async(argv):
    item_count = 0
    number_of_request = 0
    query = ''
    filename = ''

    try:
        opts, args = getopt.getopt(argv, 'q:n:r:o:', ['query,', 'number-of-request', 'item-per-request', '--output-file'])
    except getopt.GetoptError:
        print('main.py -q <query> -n <number_of_request> -r <item_per_request>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-q', '--query'):
            query = arg
        if opt in ('-n', '--number-of-request'):
            number_of_request = int(arg)
        elif opt in ('-r', '--item-per-request'):
            item_count = int(arg)
        elif opt in ('-o', '--output-file'):
            filename = arg
        else:
            item_count = 10
            number_of_request = 1

    if not query:
        print('specify query first!')
        print('main.py -q <query> -n <number_of_request> -r <item_per_request>')
        sys.exit(2)

    svc = TwitterSearchService(query=query, max_item_count=item_count)
    tws = []
    for i in range(number_of_request):
        t = await svc.get_next_results()
        if not t:
            break
        tws += t.data

    json = jsonpickle.encode({'tweets': tws}, unpicklable=False, indent=2)

    if not filename:
        print(json)
    else:
        write_file(filename, json)

asyncio.run(main_async(sys.argv[1:]))