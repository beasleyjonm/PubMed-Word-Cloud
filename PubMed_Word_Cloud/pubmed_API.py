import sys
import json
import requests as rq
import re
from collections import Counter


#Function get_ids courtesy of https://andre-rendeiro.com/2015/10/28/pubmed_wordcloud
def get_ids(term, ids=list(), retstart=0, retmax=1000000):
    """
    Return all Pubmed Ids of articles containing a term, in a recursive fashion.
    """
    base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&"
    # build query based on options
    options = list()
    options.append("term=%s" % term)
    options.append("retstart=%i" % retstart)  # restart query where it was left
    options.append("retmax=%s" % retmax)
    options.append("retmode=json")

    # get query
    url = base_url + "&".join(options)
    data = json.load(rq.get(url))

    # if there are hits, add to ids list
    if len(data["esearchresult"]["idlist"]) > 0:
        ids += data["esearchresult"]["idlist"]

        # if there is more data than retmax
        if int(data["esearchresult"]["count"]) > retmax:
            return get_ids(term, ids, retstart + int(data["esearchresult"]["retmax"]))

    # if there are no hits, return ids list
    else:
        return ids

print(get_ids("protac", 100000))