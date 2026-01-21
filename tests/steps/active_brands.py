import json
import logging
import os
import re
from pathlib import Path
from time import sleep
import requests
from behave import when, then
from tests.utilities.api_utilities import get_active_brands_id, get_token, login_with_creds, \
    get_br_homepage_url, build_link, get_homepage_bc_link, get_bc_link_from_detail
from tests.utilities.final_url import q_fin_url
from tests.utilities.url_assertion import url_assertion
import allure

logger = logging.getLogger()

@when(u'user gets list of current and new active brands')
def step_impl(context):
    context.username = os.getenv('USERNAME_USER')
    context.pwd = os.getenv('PWD_USER')
    url = os.getenv('BASE_URL_API')
    #logs in portal api and gets csrf-token as
    token = get_token()
    login_resp = login_with_creds(token, context.username, context.pwd)
    context.access_token = login_resp.json()['csrf_token']

    #gets new (today's) active brands' IDs
    context.new_ac_br_ids = set(get_active_brands_id(context.username, context.pwd, context.access_token))
    logger.info("Got today's active brands IDs\n\n")

    #gets current (yesterday's) active brands' IDs stored in repo
        # Get the directory where JTest.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the full path to the Excel file
    file_path = str(current_dir.replace("steps", "utilities/test_data/active_brands.json"))
    context.file_path = Path(file_path)

    with context.file_path.open("r") as file:
        context.content = json.load(file)
    context.current_ac_br_ids = set(context.content.get("ids"))
    logger.info("Got yesterday's active brands IDs\n")

@then(u'user will check if there would be any new brands to add to it and delete from it')
def step_impl(context):
    # comparing both new and current active brands ids to see any new or deleted brands and processing the changes.
    logger.info("Comparing yesterday's active brands IDs with today's")

    #new ids:
    context.add_ids = list(context.new_ac_br_ids.difference(context.current_ac_br_ids))

    #deleted ids:
    context.delete_ids = list(context.current_ac_br_ids.difference(context.new_ac_br_ids))

    # reporting changes, needs to get brands detail using its ID, will be updated to better of letting this know to
    logger.info(f'NEW ACTIVE BRANDS IDS: {context.add_ids}\n')
    logger.info(f'DELETED ACTIVE BRANDS IDS: {context.delete_ids}\n')

    # updates changes to context.current_ac_br_ids
    if context.add_ids:
        context.current_ac_br_ids.update(context.add_ids)
    if context.delete_ids:
        context.current_ac_br_ids.difference_update(context.delete_ids)
    context.content["ids"] = sorted(context.current_ac_br_ids, key=int)

    #writing updated current_ac_br_ids to json file
    with context.file_path.open("w") as file:
        json.dump(
            context.content,
            file,
            indent=1,
            separators=(",", ": ")
        )
        file.write("\n")
    logger.info("Updated changes to current active brands IDs list and wrote it back to the file")
    logger.info("Wrote updated active brands' IDs back to the file")


@when(u'user gets BC links for all active brands homepage')
def step_impl(context):
    #get stored homepage urls from activa_brands.json
    with context.file_path.open("r") as file:
        context.content = json.load(file)
    context.current_ac_br_urls = context.content["ids-urls"]
    logger.info("Got stored homepage URLS")

    #get homepage urls for new active current brands and add them to urls and get urls for delete_ids and delete them from urls
    context.new_urls = {}
    context.deleted_urls = {}
    if context.add_ids:
        for id in context.add_ids:
            if '1424' == id:
                homepage_url = "https://amazon.com?tag=cs-vs-1600"
            elif '1368' == id:
                homepage_url = "https://www.amazon.com/stores/FoodSaver/page/AC9726F6-C85C-441D-A56F-BE15C5F527D2?tag=cs-vs-1601"
            else:
                homepage_url = get_br_homepage_url(context.username, context.pwd, context.access_token, id)
                sleep(0.5)

            context.current_ac_br_urls[id] = homepage_url
            context.new_urls[id] = homepage_url
            logger.info(f"Added new active brand's homepage to current active brands' homepage urls: {id} : {homepage_url}")

    if context.delete_ids:
        for id in context.delete_ids:
            homepage_url = context.current_ac_br_urls.get(id)
            try:
                del context.current_ac_br_urls[id]
            except KeyError:
                print(f"{id} was not in current_ac_br_urls")
            context.deleted_urls[id]=homepage_url
            logger.info(f"Deleted inactive brand's homepage url from current active brands' homepage urls: {id} : {homepage_url}")
            sleep(0.5)

    logger.info("Checking if number of IDs and URL are equal")
    if len(context.current_ac_br_urls) < len(context.current_ac_br_ids):
        context.extra_key = [item for item in context.current_ac_br_ids if item not in context.current_ac_br_urls]
        logger.critical(f'EXTRA IDS: {context.extra_key}')
    if len(context.current_ac_br_urls) > len(context.current_ac_br_ids):
        context.extra_key = [key for key in context.current_ac_br_urls if key not in context.current_ac_br_ids]
        logger.critical(f'EXTRA URLS: {context.extra_key}')


    #assign updated ids-urls back to context.content:
    context.content["ids-urls"] = dict(sorted(context.current_ac_br_urls.items(), key=lambda item: int(item[0])))
    #print(f'ids-urls: {context.content["ids-urls"]}\n\n')

    #writes updated urls back to active_brands.json file
    with context.file_path.open("w") as file:
        json.dump(
            context.content,
            file,
            indent=1,
            separators=(",", ": ")
        )
        file.write("\n")
    logger.info("Wrote updated homepage urls back to the file")

@when(u'user will check BC links are working, if not user will report it')
def step_impl(context):
    #gets stored BC links from active_brands.json
    with context.file_path.open("r") as file:
        context.content = json.load(file)
    context.current_ac_br_links = context.content.get("ids-links")
    logger.info("Got stored BC links from the file")

    context.new_links = {}
    context.deleted_links = {}
    #updates links based on new or deleted ids
    if context.new_urls:
        for key in context.new_urls.items():
            try:
                bc_link = (build_link(context.access_token,'USER', 'USER', key[1], 'false'))
                if bc_link.status_code == 200:
                    bc_link = bc_link.json().get('url_long')
                else:
                    bc_link.raise_for_status()
                #print(bc_link)

                # Tried to cut long links but some brands links doesn't work
                # pattern = r"aff_id=9297"
                # match = re.search(pattern, bc_link)
                # if match:
                #     split_point = match.end()
                #     bc_link = bc_link[:split_point]

                #print(f"bc_HOMEPAGE_LINK: {bc_link} for {key}\n")
                sleep(0.5)
                #here 403 is the status code for brands' urls that has not been activated for deeplinking.
            except requests.RequestException:
                bc_link = get_bc_link_from_detail('USER', 'USER', context.access_token, key[0])
                sleep(0.5)
            context.new_links[key[0]] = bc_link
            context.current_ac_br_links[key[0]] = bc_link
        logger.info(f"Added new active brands' BC links {context.new_links}")

    if context.deleted_urls:
        for key in context.deleted_urls.keys():
            if key in context.current_ac_br_links:
                context.deleted_links[key] = context.current_ac_br_links[key]
                del context.current_ac_br_links[key]
        logger.info(f"Deleted inactive brands' BC links {context.deleted_links}")

    #print(context.current_ac_br_links)
    #write updated links back to the file - do it
    context.content["ids-links"] = dict(sorted(context.current_ac_br_links.items(), key=lambda item: int(item[0])))
    with context.file_path.open("w") as file:
        json.dump(
            context.content,
            file,
            indent=1,
            separators=(",", ": ")
        )
        file.write("\n")
    logger.info("Wrote updated BC links back to file")

    #check if updated current active brands' bc links land on their destination urls
    context.issue_brands = []
    #print(f'last steps ids-links: {context.current_ac_br_links}')
    for id in context.current_ac_br_links.items():
        if context.current_ac_br_links[id[0]] is None:
            print(f"PRINT __ THIS BRAND GOT A null for it's brand_url: {id}\n")
            id = (id[0] + f"this brand got null for it's brand_url {context.current_ac_br_links[id[0]]}")
            context.issue_brands.append(id)
        elif 'Look into This' in context.current_ac_br_links[id[0]]:
            print(f"PRINT __ THIS BRAND needs to be Looked: {id}\n")
            id = (id[0] + f"this brand needs to be looked it's brand_url {context.current_ac_br_links[id[0]]}")
            context.issue_brands.append(id)
        else:
            final_url = q_fin_url(id[1], context.current_ac_br_urls[id[0]])
            #print(f"final_url: {final_url}\n\n")
            if final_url is None:
                print(f"PRINT __ THIS BRAND GOT A PROBLEM, None: {id}\n\n")
                context.issue_brands.append(id)
            elif "Not Active" in final_url:
                print(f"PRINT __ THIS BRAND GOT A PROBLEM, Not Active: {id}")
                print(f"id[0]: {context.current_ac_br_urls[id[0]]}\n\n")
                id = (id[0] + ": " + final_url, id[1])
                context.issue_brands.append(id)
            elif "Look into This" in final_url:
                print(f"PRINT __ THIS BRAND GOT A PROBLEM, Look: {id}")
                print(f"id[0]: {context.current_ac_br_urls[id[0]]}\n\n")
                id = (id[0] + ": " + final_url, id[1])
                context.issue_brands.append(id)
            #else:
                #url_assertion(context.current_ac_br_urls[id[0]], final_url)
                #final_url assert the domains anyways
    print(f'ISSUE BRANDS: {context.issue_brands}\n\n')
    #print(f'ALL IDS: {sorted(context.new_ac_br_ids, key=int)}\n')
    #logger.critical(f'ALL IDS: {sorted(context.new_ac_br_ids, key=int)}\n')
    #logger.critical(f'ISSUE BRANDS: {context.issue_brands}\n\n')

    #attaching active_brands.json and ISSUE Brands
    data = {
        "ISSUE BRANDS": context.issue_brands,
        "active_brands.json" : context.content

    }
    allure.attach(
        json.dumps(data, indent=2),
        name="Active Brands",
        attachment_type=allure.attachment_type.JSON
    )
