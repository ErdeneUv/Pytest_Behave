import json
import logging
import os
import re
from email.utils import unquote
from pathlib import Path

import requests
from urllib.parse import urlparse
import tldextract
from pandas.core.computation.common import result_type_many
from ua_generator import generate

logger = logging.getLogger()

def share_a_sale(resp):
    print(f'starting share_a_sale with {resp}')
    try:
        session = requests.Session()
        ua = get_ua('chrome')
        session.headers.update({'User-Agent': ua})
        session.max_redirects = 7
        share_resp = session.get(resp)
        body = share_resp.text
        pattern = r"window\.location\.replace\('(.+?)'\)"
        match = re.search(pattern, body)
        if match:
            #print(f'MATCH: {match}')
            sale_a_share_url = match.group(1).replace('\\/', '/')
            print(f'MATCH URL: {sale_a_share_url}')
            return sale_a_share_url
        elif 'inactive' in body:
            print(f'Inactive Brand: {resp}')
            return "Not Active"
        else:
            print(f'No URL found in sale_a_share resp body: {str(body)} in resp: {resp}')
    except Exception as e:
        print(f'Exception in share a sale: {str(e)}')


def q_fin_url(bc_link, brand_url):
    domain_brand_url = extract_https(brand_url)
    print(f'Brand in q_fin_url : {brand_url}')
    print(f'BC LINK in q_fin_url: {bc_link}')
    session = requests.Session()
    ua = get_ua('chrome')
    session.headers.update({'User-Agent': ua})
    session.max_redirects = 7
    brands_possible = {}

    verify_ssl = True
    if 'toms.com' in brand_url:
        verify_ssl = False
    try:
        response = session.get(str(bc_link), allow_redirects=True, verify=verify_ssl, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f'Request Failed: {e}\n\n')
        return fin_url(bc_link, brand_url)
    url_link_landed = response.url

    if 403 == response.status_code and 'https://www.adidas.com/us?clickId' in response.url:
        actual_domain = extract_https(response.url)
        return actual_domain
    if 200 == response.status_code:
        actual_domain = extract_https(url_link_landed)
        if actual_domain == domain_brand_url:
            print(f'Landed: {url_link_landed}\n\n')
            return url_link_landed
        else:
            resp = session.get(url_link_landed, allow_redirects=True, timeout=10)
            actual_domain = extract_https(resp.url)
            if actual_domain == domain_brand_url:
                print(f'Landed: {resp.url}\n\n')
                return resp.url
            elif 'shareasale' in resp.url:
                shareasale_link = share_a_sale(url_link_landed)
                actual_domain = extract_https(shareasale_link)
                if actual_domain == domain_brand_url:
                    print(f'Landed: {shareasale_link}\n\n')
                    return shareasale_link
            else:
                brands_possible[bc_link] = brand_url
                return fin_url(bc_link, brand_url)
    else:
        brands_possible[bc_link] = brand_url
        return fin_url(bc_link, brand_url)

    file_path = Path('/Users/erden/repos/brandcycle-test/tests/utilities/test_data/brands_possible.json')
    with open(file_path, 'w') as pos_file:
        json.dump(brands_possible, pos_file, indent=4)



def fin_url(bc_link, brand_url):
    session = requests.Session()
    ua = get_ua('chrome')
    session.headers.update({'User-Agent': ua})
    session.max_redirects = 7
    is_redir = True
    location = ''
    print(f"Start of fin_url\ngot this BC link: {bc_link} and this Brand URL: {brand_url} in final_url\n")

    check_brand_url = extract_https(brand_url)
    #follows redirects one by one check status code if 300s look for next redirect link in Locations, Refresh and JS redirection
    max_redirects = 10
    redirect_count = 0

    try:
        while is_redir:
            if redirect_count >= max_redirects:
                return "Too many redirects"
            redirect_count += 1
            print(f'\nRedirect count: {redirect_count}')

            # some how toms.com having hard time with SSL verification

            response = session.get(str(bc_link), allow_redirects=False)
            print(f'Redirect : {response.url} \n')

            if 300 <= response.status_code < 400:
                if response.headers.get('Location'):
                    location = response.headers.get('Location')
                elif response.headers.get('Refresh'):
                    try:
                        location = response.headers.get('Refresh')
                        match = re.search(r'url\s*=\s*(.+)', location, re.IGNORECASE)
                        if match:
                            location = match.group(1).strip()
                    except Exception as e:
                        raise Exception(f"No refresh header here: {response.headers.get('Refresh')}") from e
                else:
                    try:
                        #looking for JS redirect in the HTML body
                        location = re.search(
                            r"""window\.location(?:\.replace)?\(['"]([^'"]+)['"]\)""",
                            response.text,
                            flags=re.IGNORECASE
                        )
                        print(f'Location found in 300-400 -> JS: {location}')
                    except Exception as e:
                        raise RuntimeError(f"Did not find a JS redirect to {brand_url} in the last response.") from e

            if 'shareasale' in location:
                print(f'got shareasale in location in fin_url2: {location}')
                shareasale_url = share_a_sale(location)
                actual_domain = extract_https(shareasale_url)
                if actual_domain == check_brand_url:
                    return actual_domain
                else:
                    return "Not Active"
            if 200 == response.status_code and "closed" in response.url:
                print(f"GOT 200: {response.status_code} \n and text: {response.text}\n")
                return "Not Active"

            if 400 <= response.status_code < 500:
                if 'https://www.adidas.com/us?clickId' in response.url:
                    actual_domain = extract_https(response.url)
                    return actual_domain
                else:
                    print(f"GOT 400s: {response.status_code} \n and text: {response.text}\n")
                    return "Not Active"
            if 200 == response.status_code and "error" in response.url:
                print(f"GOT 200: {response.status_code} \n and text: {response.text}\n")
                return "Not Active"
            if 200 == response.status_code and 'linksynergy.com' in location:
                try:
                    location = response.headers.get('Refresh')
                    match = re.search(r'url\s*=\s*(.+)', location, re.IGNORECASE)
                    if match:
                        location = match.group(1).strip()
                except Exception as e:
                    raise Exception(f"No refresh header here: {response.headers.get('Refresh')}") from e

            check_location = extract_https(str(location))
            #print(f'CHECK Location: {check_location}')
            if "Not Active" in check_location:
                return check_location
            elif check_brand_url in check_location:
                print(f"{check_brand_url} is in {check_location}\n")
                return location
            elif bc_link == location:
                print(f"bc link: {bc_link} and location: {location} are same creating loop!\n")
                resp = session.get(location, allow_redirects=True, timeout=10)
                if bc_link == resp.url:
                    print(f'still in the loop after following location further needs to be checked!')
                    return "Look into This it's been looping in location header"
                else:
                    bc_link = location
            else:
                bc_link = location
        return location
    except Exception as e:
        print(f'Error processing {location} in {bc_link}: {e}')


def extract_https(url):
    # A reason to strip to the domain name is https://www.samsclub.com/are-you-human?
    """Extracts and normalizes the bare domain from a URL (e.g. example)."""
    try:
        if ' ' in url:
            url = url.split(' ')[0]

        if "Not Active" in url:
            return url
        elif "app.link" in url:
            extractor = tldextract.TLDExtract(extra_suffixes=["app.link"])
            extracted = extractor(url).domain
            return extracted
        else:
            extracted = tldextract.extract(url).domain
            return extracted.lower()
    except Exception as e:
        print(f'Error processing extract_https {url}: {e}')

def extract_by_slash(url):
    count_slashes = url.count('/')
    if count_slashes >2:
        split_index = url.rfind('/')
        first_part = url[:split_index]
        return first_part
    else:
        return url

def get_ua(browser):
    user_agents = generate(device='desktop', browser=browser)
    return user_agents.text

def shareasale(bc_link, brand_url):
    f"""
        Follow HTTP redirects (and a final JS-based redirect) to ensure we land on given url

        Args:
            url: The initial affiliate link to request, and brand's homepage url to compare.

        Returns:
            The final URL (which will be on example.com) that matches homepage url

        Raises:
            RuntimeError: If we cannot resolve to give url.
        """
    check_brand_url = extract_https(brand_url)
    ua = get_ua('chrome')
    session = requests.Session()
    session.headers.update({
        "User-Agent": ua
    })
    # 1) Follow standard HTTP redirects
    resp = session.get(bc_link, allow_redirects=True)
    final_url = resp.url

    # 2) If requests already landed on given url, we're done
    if urlparse(final_url).hostname and brand_url in urlparse(final_url).path:
        return final_url
    if "notactive" in urlparse(final_url).path:
        logger.warning(f"THIS BRAND IS NOT ACTIVE: {brand_url}\n")
        print(f"This brand is not active on shareasale: {brand_url} THIS IS WHAT RETURNED: {urlparse(final_url).path}\n")
        return "Not Active: Shareasale"

    # 3) Otherwise look for JS redirect in the HTML body
    js_redirect = re.search(
        r"""window\.location(?:\.replace)?\(['"]([^'"]+)['"]\)""",
        resp.text,
        flags=re.IGNORECASE
    )
    if not js_redirect:
        raise RuntimeError(
            f"Did not find a JS redirect to {brand_url} in the last response."
        )

    # 4) Extract and unquote the redirect target
    raw_target = js_redirect.group(1)
    clean_target = raw_target.replace(r"\/", "/")
    target_url = unquote(clean_target)

    # 5) Issue a final GET (no further redirects expected)
    resp2 = session.get(target_url, allow_redirects=True)
    final_url2 = resp2.url

    # 6) Verify domain
    print(f"check_final_url: {final_url2}\nbrand_url: {check_brand_url}")

    if check_brand_url not in final_url2:
        raise RuntimeError(
            f"Final URL did not land on {check_brand_url}, instead it got {final_url2})"
        )
    else:
        return final_url2


if __name__ == "__main__":
    """
    file_path = "/Users/erden/repos/brandcycle-test/tests/utilities/test_data/active_brands.json"
    file_path = Path(file_path)

    with file_path.open("r") as file:
        content = json.load(file)
    current_ac_br_ids = set(content.get("ids"))
    current_ac_br_url = content.get("ids-urls")
    current_ac_br_link = content.get("ids-links")
    final_all = {}
    for id in current_ac_br_ids:
        brand_url = current_ac_br_url[id]
        link = current_ac_br_link[id]
        final = q_fin_url(link, brand_url)
        final_all[id] = final
    print(f'WHAT q_fin_url returns: {final_all}')
    
    """

    brand_url = 'https://www.nike.com/'
    link = 'https://brandcycle.go2cloud.org/aff_c?offer_id=1222&aff_id=9297&url=https%3A%2F%2Fwww.jdoqocy.com%2Fclick-7921344-17049705%3Fsid%3DA%7Baffiliate_id%7DO%7Boffer_id%7DTID%7Btransaction_id%7D%26url%3Dhttps%253A%252F%252Fwww.nike.com&aff_unique3=9853e9c9-fb92-4322-90f3-e02889c1dd96'
    final = q_fin_url(link, brand_url)
    print(f'WHAT q_fin_url returns: {final}')

"""
    result_file_path = Path('/Users/erden/repos/brandcycle-test/tests/utilities/test_data/final_result.json')

    with result_file_path.open("w") as file:
        json.dump(
            final,
            file,
            indent=1,
            separators=(",", ": ")
        )
        file.write("\n")
        """
