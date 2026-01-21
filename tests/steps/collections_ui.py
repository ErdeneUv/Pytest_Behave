from behave import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from tests.pages.collection_page import CollectionPage


@then("user should see Collection Header, Creator info")
def step_impl(context):
    context.collection_page = CollectionPage(context.driver)
    context.collection_page.avatar_img.click()
    assert context.collection_page.avatar_img.is_displayed(), f"avatar image is not displayed"
    assert context.collection_page.creator_name.is_displayed(), f"creator name is not displayed"
    assert context.collection_page.edit_creator_info_button.is_displayed(), f"edit creator info button is not displayed"


@then("user should see 'Published', 'Draft' and 'Archive' tab buttons, and 'New Collection' button")
def step_impl(context):
    context.collection_page.published_tab_button.is_displayed(), f"published tab button is not displayed"
    context.collection_page.drafts_tab_button.is_displayed(), f"draft tab button is not displayed"
    context.collection_page.archived_tab_button.is_displayed(), f"archive tab button is not displayed"
    context.collection_page.new_collection_button.is_displayed(), "'New Collection' button is not visible"


@then("user should see a published Collection named '{coll_name}', it's image, 'Edit', 'View' and 'Url Copy' buttons")
def step_impl(context, coll_name):
    elements = context.collection_page.elements(context.collection_page.COLLECTION_NAME)
    collections_names = [el.text for el in elements]

    collections_imgs = context.collection_page.elements(context.collection_page.COLLECTION_IMG)

    assert coll_name in collections_names, f"collection name: {coll_name} is not in collection names: {collections_names}"
    for img in collections_imgs:
        assert img.is_displayed(), f"collection image is not displayed"
    assert context.collection_page.collection_edit_btn.is_displayed(), f"edit btn is not displayed"
    assert context.collection_page.collection_view_btn.is_displayed(), f"view btn is not displayed"


@when("user clicks on 'New Collection'")
def step_impl(context):
    context.collection_page.new_collection_button.click()


@when('user enters "Test Automation Collection" in Collection name field')
def step_impl(context):
    context.collection_page.collection_name_input.click()
    context.collection_page.collection_name_input.type("Test Automation Collection")


@then('user should see "Collection Name" crossed out and got green check mark in Summary')
def step_impl(context):
    assert context.collection_page.collection_name_checker.is_displayed(), "Collection Name Checker is not displayed"


@when('user clicks on "Create" button')
def step_impl(context):
    context.collection_page.create_btn.click()


@when("user uploads Collection Hero image")
def step_impl(context):
    context.collection_page.upload_img('hero.jpeg')


@when("user enters '{coll_desc}' Collection Description and store Collection's url.")
def step_impl(context, coll_desc):
    context.collection_page.collection_description.click()
    context.collection_page.collection_description.type(coll_desc)


@step("user clicks on 'Update' button")
def step_impl(context):
    context.wait.until(ec.presence_of_element_located(context.collection_page.UPLOAD_HERO_IMG_CHECKER))
    context.collection_page.update_collection_btn.click()


@then("user clicks on 'Draft' button and assert '{expected_name}' in collection names")
def step_impl(context, expected_name):
    context.collection_page.drafts_tab_button.click()
    elements = context.collection_page.elements(context.collection_page.COLLECTION_NAME)
    collection_names = [el.text for el in elements]

    assert expected_name in collection_names


@then("user stores Hero images uuid, avatar images uuid")
def step_impl(context):
    context.wait.until(ec.visibility_of_element_located(context.collection_page.first_collection_img))
    img_src = context.collection_page.first_collection_img.get_dom_attribute("src")
    context.img_uuid = img_src.split("/")[-1]
    print(f'img_src: {img_src}\n\n\n\n')
    print(f'img_uuid: {context.img_uuid}\n\n\n\n')

    avatar_src = context.collection_page.avatar_img.get_attribute("src")
    context.avatar_uuid = avatar_src.split("/")[-1]


@when("user clicks on 'Edit' button of the collection created")
def step_impl(context):
    context.collection_page.collection_edit_btn.click()


@when("user scroll down to \'Add a new item to this Collection\' and adds items with following Kohl\'s Url in Destination Url")
def step_impl(context):
    context.actions = ActionChains(context.driver)
    context.actions.move_to_element(context.collection_page.destination_url_input.webelement).perform()
    for row in context.table:
        url = row[0]
        context.collection_page.add_item(destination_url=url, monetize=False)
        context.wait.until(ec.visibility_of_element_located(context.collection_page.ADD_ITEM_CHECKER))

@when("user clicks on 'Monetize this link' button")
def step_impl(context):
    context.collection_page.monetize_btn_collection.click()

@when("user clicks on \'Add a new item to this Collection\' and enters Kohl\'s Url in Destination Url")
def step_impl(context):
    for row in context.table:
        url = row[0]
        context.collection_page.add_item(destination_url=url, monetize=True)
        context.wait.until(ec.visibility_of_element_located(context.collection_page.ADD_ITEM_CHECKER))

@then("user should see three items in the Collection Items with following names")
def step_impl(context):
    expected_names = [row[0] for row in context.table]
    actual_names = context.collection_page.get_item_names_any_view()
    for name in expected_names:
        assert any(name in actual for actual in actual_names), f"{name} not found in {actual_names}"

@then("user should see two affiliate link and one Kohl's url in affiliate link button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    buttons = context.collection_page.shopper_item_view_product_btn
    assert len(buttons) >= 3, "Expected at least three affiliate buttons"


@when('user clicks on "Edit" button on second from the top Collection Item')
def step_impl(context):
    edit_buttons = context.collection_page.elements(context.collection_page.ITEM_EDIT_BTN_1)
    if len(edit_buttons) < 2:
        raise AssertionError("Less than two items available to edit")
    edit_buttons[1].click()


@step("updates Item names to \"Monarch Cupholder End Table, Brown UPDATED\" and Store to Kohl's UPDATED")
def step_impl(context):
    context.collection_page.item_name_input.clear_all()
    context.collection_page.item_name_input.type("Monarch Cupholder End Table, Brown UPDATED")
    context.collection_page.store_input.clear_all()
    context.collection_page.store_input.type("Kohl's UPDATED")


@step("clicks on Update Item")
def step_impl(context):
    context.collection_page.update_item_popup_btn.click()


@then("User should see 'UPDATED' in Collection name and Store")
def step_impl(context):
    names = context.collection_page.get_item_names_any_view()
    assert any("UPDATED" in name for name in names), f"UPDATED not present in names {names}"


@step("user stores item images uuid")
def step_impl(context):
    imgs = context.collection_page.shopper_item_img
    if not imgs:
        raise AssertionError("No item images found to store uuid")
    context.item_img_uuid = [img.get_attribute("src").split("/")[-1] for img in imgs]


@when("user clicks on 'Reorder Product'")
def step_impl(context):
    context.collection_page.reorder_items_btn.click()


@step("user drags the top item to the bottom")
def step_impl(context):
    cards = context.collection_page.admin_item_cards
    if len(cards) < 2:
        raise AssertionError("Need at least two items to reorder")
    actions = ActionChains(context.driver)
    actions.drag_and_drop(cards[0], cards[-1]).perform()


@step("user clicks on 'Save Reorder' button")
def step_impl(context):
    context.collection_page.save_reorder_btn.click()


@then("user should see top item with 'UPDATE' in it's name")
def step_impl(context):
    names = context.collection_page.get_item_names_any_view()
    assert names and "UPDATED" in names[0], f"Top item name does not include UPDATED: {names}"


@when("user clicks on 'Remove' button of top item")
def step_impl(context):
    context.collection_page.item_remove_btn_1.click()


@step("user clicks on 'Remove Item' button on pop up")
def step_impl(context):
    remove_btn = (By.XPATH, "//button[contains(., 'Remove Item')]")
    context.wait.until(ec.element_to_be_clickable(remove_btn))
    context.driver.find_element(*remove_btn).click()


@then("user should see only two items")
def step_impl(context):
    context.wait.until(lambda d: len(context.collection_page.admin_item_cards) == 2)


@step("user should not see 'Monarch Cupholder End Table, Brown UPDATED\" and Store to Kohl's UPDATED' in item names")
def step_impl(context):
    names = context.collection_page.get_item_names_any_view()
    assert not any("UPDATED" in name for name in names), f"Unexpected UPDATED item still present: {names}"


@when("user clicks on 'Preview' button")
def step_impl(context):
    context.collection_page.view_collection_btn.click()


@then("user should navigate to the url that has /preview in it")
def step_impl(context):
    context.collection_page.wait_url_contains("/preview")


@when("user clicks on 'View' button")
def step_impl(context):
    context.collection_page.open_collection_from_list(action="view")


@then("user should see the collection with the name of 'Test Automation Collection' in a new tab")
def step_impl(context):
    context.driver.switch_to.window(context.driver.window_handles[-1])
    assert "Test Automation Collection" in context.collection_page.shopper_collection_name.get_text()


@then("user should see the two collection items")
def step_impl(context):
    items = context.collection_page.shopper_item_cards
    assert len(items) >= 2, "Expected at least two collection items"


@then(u'user should see item\'s img, store, name, and view product button.')
def step_impl(context):
    assert context.collection_page.shopper_item_img, "Item image not visible"
    assert context.collection_page.shopper_item_name, "Item name not visible"
    assert context.collection_page.shopper_item_store, "Item store not visible"
    assert context.collection_page.shopper_item_view_product_btn, "View product button not visible"


@then(u'user should see \'https://www.kohls.com/product/prd-4544860/shark-pet-cordless-stick-vacuum-ix141.jsp\' in url')
def step_impl(context):
    context.collection_page.wait_url_contains("shark-pet-cordless-stick-vacuum-ix141")



@then("user should see the Hero image and Description")
def step_impl(context):
    assert context.collection_page.shopper_hero_img.is_displayed(), "Hero image is not visible"
    assert context.collection_page.collection_description.is_displayed(), "Description is not visible"


@then("user should see Creators info and avatar image and goes back to Collection Admin page")
def step_impl(context):
    assert context.collection_page.shopper_creator_name.is_displayed(), "Creator name missing"
    assert context.collection_page.shopper_avatar_img.is_displayed(), "Avatar image missing"
    context.driver.close()
    context.driver.switch_to.window(context.driver.window_handles[0])


@when("user stores Shopper page's url")
def step_impl(context):
    context.shopper_url = context.driver.current_url


@then("user should see 'Set Name', 'Upload a hero image', 'Add at least 1 item' crossed out and got a green check marks")
def step_impl(context):
    assert context.collection_page.is_setup_checklist_complete(), "Setup checklist not complete"


@when("user clicks on 'Publish' button on Collection edit page")
def step_impl(context):
    context.collection_page.publish_collection_btn.click()


@then("user should see 'Test Automation Collection' in the published tab")
def step_impl(context):
    context.collection_page.switch_tab("published")
    names = [el.text for el in context.collection_page.collection_cards]
    assert any("Test Automation Collection" in name for name in names)


@then("user should see item's img, store, name, and view product button\.")
def step_impl(context):
    assert context.collection_page.shopper_item_img, "Item image not visible"
    assert context.collection_page.shopper_item_store, "Item store not visible"
    assert context.collection_page.shopper_item_name, "Item name not visible"
    assert context.collection_page.shopper_item_view_product_btn, "View product button not visible"


@when("user clicks on 'view product' button")
def step_impl(context):
    context.collection_page.shopper_item_view_product_btn[0].click()


@then("user should see 'https://www\.kohls\.com/product/prd-4544860/shark-pet-cordless-stick-vacuum-ix141\.jsp' in url")
def step_impl(context):
    context.collection_page.wait_url_contains("shark-pet-cordless-stick-vacuum-ix141")


@when("user goes back to Collection Admin page and copies the Collection's Url")
def step_impl(context):
    context.driver.switch_to.window(context.driver.window_handles[0])
    context.collection_page.collection_copy_btn.click()
    context.copied_collection_url = context.collection_page.collection_copy_btn.get_attribute("data-clipboard-text") or context.driver.current_url


@then("Collection's url matches with published collection's url")
def step_impl(context):
    assert context.copied_collection_url in context.shopper_url or context.shopper_url in context.copied_collection_url


@when("user clicks on 'Edit' button on the collection")
def step_impl(context):
    context.collection_page.open_collection_from_list(action="edit")


@step("user clicks on 'Archive' button")
def step_impl(context):
    context.collection_page.archive_collection_btn.click()


@when("user clicks on 'Archive' tab")
def step_impl(context):
    context.collection_page.switch_tab("archived")


@then("user should see the Collection with the name 'Test Automation Collection'")
def step_impl(context):
    names = [el.text for el in context.collection_page.collection_cards]
    assert any("Test Automation Collection" in name for name in names)


@when("user clicks on 'Edit' button on 'Test Automation Collection' collection")
def step_impl(context):
    names = context.collection_page.elements(context.collection_page.COLLECTION_NAME)
    edit_buttons = context.collection_page.elements(context.collection_page.COLLECTION_EDIT_BTN)
    target_clicked = False
    for idx, el in enumerate(names):
        if "Test Automation Collection" in el.text:
            edit_buttons[idx].click()
            target_clicked = True
            break
    assert target_clicked, "Target collection not found to edit"


@step("user clicks on 'Delete' button")
def step_impl(context):
    context.collection_page.delete_collection_btn.click()


@step("user clicks on 'Delete Collection' button on pop up")
def step_impl(context):
    delete_btn = (By.XPATH, "//button[contains(., 'Delete Collection')]")
    context.wait.until(ec.element_to_be_clickable(delete_btn))
    context.driver.find_element(*delete_btn).click()


@then("user should not see the 'Test Automation Collection' Collection in Archive tab")
def step_impl(context):
    names = [el.text for el in context.collection_page.collection_cards]
    assert not any("Test Automation Collection" in name for name in names)


@step("user should get 404 following the Collection's url")
def step_impl(context):
    context.driver.get(context.copied_collection_url)
    assert "404" in context.driver.page_source or context.driver.title.startswith("404")
