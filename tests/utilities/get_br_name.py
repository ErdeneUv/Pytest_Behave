import tldextract
import re

def get_br_name(url):
    """
    Extracts the second-level domain name from a URL.
    :param url:
    :return: main domain name
    """

    #checks if url is just a word
    if re.fullmatch(r'[a-zA-Z0-9-]+', url):
        return url

    #handles if url is just a domain like example.com
    if re.fullmatch(r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}', url):
        ext = tldextract.extract(url)
        if ext.domain:
            return ext.domain
        else:
            return url

    #finally it assumes url is complete url
    ext = tldextract.extract(url)
    return ext.domain

