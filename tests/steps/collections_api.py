"""
Step definitions for the BrandCycle collections API tests.

These steps drive the scenarios defined in ``collection.feature``.  Each step uses helper functions from ``api_utilities.py`` in utilities to exercise the API.
The responses are stored on the Behave context so that subsequent steps can reference the last response or IDs extracted from it.  Status codes and
the presence of identifiers are asserted to verify expected behaviour.

Note that environment variables such as ``BASE_URL_API``, ``COLLECTION``,
``COLLECTION_ITEMS``, ``USERNAME_erd`` and ``PWD_erd`` must be defined
externally for these helpers to reach the correct API endpoint with
appropriate credentials.  The defaults in ``coll.py`` assume a user
named "erd"; adjust the ``user`` parameter when calling these
functions if you have different credentials.
"""

import json
import os
from behave import given, when, then
from tests.utilities.api_utilities import create_collection, create_collection_item, update_collection_item, \
    update_collection, get_collection_for_user, get_collection_for_collection, get_collection_item, \
    delete_collection_item, delete_collection



@given('a valid user with id "{user_id}"')
def step_given_user(context, user_id):
    """Store the provided user identifier on the context for later use."""
    context.user_id = str(user_id)


@when('the user creates a collection with name "{name}", description "{description}" and default image url "{image_url}"')
def step_create_collection(context, name, description, image_url):
    """Invoke the create_collection helper and save the response.

    The collection ID extracted from the response body will be stored in a
    later step via ``save the collection id``.
    """
    # Create the collection; rely on default status of "draft" unless the
    # scenario explicitly specifies otherwise.
    response = create_collection(
        user_id=context.user_id,
        name=name,
        description=description,
        image_url=image_url,
    )
    context.last_response = response


@then('the response status code should be "{status_code}"')
def step_assert_status_code(context, status_code):
    """Assert that the most recent API response returned the expected status code."""
    actual = str(context.last_response.status_code)
    assert actual == str(status_code), f"Expected status code {status_code} but got {actual} and msg {context.last_response}"


@then('save the collection id')
def step_save_collection_id(context):
    """Extract and store the collection ID from the last response."""

    try:
        body = context.last_response.json()
        context.collection_id = str(body["data"]["id"])
    except Exception as e:
        raise AssertionError(f"Unable to extract collection ID. last response: {context.last_response} error: {e}")

@when('the user creates a collection item with name "{name}", original url "{original_url}", shopping url "{shopping_url}", store "{store}", image url "{image_url}"')
def step_create_collection_item(context, name, original_url, shopping_url, store, image_url):
    """Create a new collection item associated with the previously stored collection."""
    response = create_collection_item(
        collection_id=context.collection_id,
        name=name,
        original_url=original_url,
        shopping_url=shopping_url,
        store=store,
        image_url=image_url,
    )
    context.last_response = response


@then('save the collection item id')
def step_save_collection_item_id(context):
    """Extract and store the collection item ID from the last response."""
    try:
        body = context.last_response.json()
        context.collection_item_id = str(body["data"]["id"])
    except Exception as e:
        raise AssertionError(f"Unable to extract collection item ID. last response: {context.last_response}: {e}")


@when('the user updates the collection item with name "{name}", original url "{original_url}", shopping url "{shopping_url}", store "{store}", image url "{image_url}"')
def step_update_collection_item_full(context, name, original_url, shopping_url, store, image_url):
    """Update the collection item with the provided attributes."""
    response = update_collection_item(
        context.collection_item_id,
        name=name,
        original_url=original_url,
        shopping_url=shopping_url,
        store=store,
        image_url=image_url,
    )
    context.last_response = response


@when('the user updates the collection item with name "{name}", original url "{original_url}", shopping url "{shopping_url}"')
def step_update_collection_item_partial(context, name, original_url, shopping_url):
    """Update the collection item when only a subset of attributes are provided."""
    response = update_collection_item(
        context.collection_item_id,
        name=name,
        original_url=original_url,
        shopping_url=shopping_url,
    )
    context.last_response = response


@when('the user updates the collection to description "{description}" and status "{status}"')
def step_update_collection(context, description, status):
    """Update the collection description and/or status."""
    response = update_collection(
        context.collection_id,
        description=description,
        status=status,
    )
    context.last_response = response


@when('the user retrieves collections for the user')
def step_get_collections_for_user(context):
    """Retrieve collections belonging to the stored user ID."""
    response = get_collection_for_user(context.user_id)
    context.last_response = response


@then('the collection id should be present in the response')
def step_assert_collection_in_response(context):
    """Verify that the previously saved collection ID appears in the collections list."""
    try:
        body = context.last_response.json()
    except Exception:
        raise AssertionError("Response does not contain valid JSON from which to verify presence of collection ID")
    data_section = body.get('data', [])
    ids = []
    if isinstance(data_section, list):
        for item in data_section:
            ids.append(str(item.get('id')))
    elif isinstance(data_section, dict):
        ids.append(str(data_section.get('id')))
    found = str(context.collection_id) in ids
    assert found, f"Collection ID {context.collection_id} not found in response data {ids}"


@then('the collection name should be "{name}" and description should be "{description}"')
def step_assert_collection_name_description(context, name, description):
    """Assert that the most recent collection response contains the expected name and description."""
    try:
        body = context.last_response.json()
    except Exception:
        raise AssertionError("Response does not contain valid JSON to assert collection attributes")
    attributes = None
    if isinstance(body, dict):
        data_section = body.get('data')
        # If the response wraps a single collection
        if isinstance(data_section, dict):
            attributes = data_section.get('attributes', {})
        # If the response is a list of collections (e.g. get_collection_for_user)
        elif isinstance(data_section, list):
            # Find the collection matching the saved ID
            for item in data_section:
                if str(item.get('id')) == str(getattr(context, 'collection_id', None)):
                    attributes = item.get('attributes', {})
                    break
    if not attributes:
        raise AssertionError("No attributes found in response to assert collection name and description")
    actual_name = attributes.get('name')
    actual_description = attributes.get('description')
    assert actual_name == name, f"Expected collection name '{name}' but got '{actual_name}'"
    assert actual_description == description, f"Expected collection description '{description}' but got '{actual_description}'"


@then('the collection item name should be "{name}" and original url should be "{original_url}"')
def step_assert_collection_item_name_original(context, name, original_url):
    """Assert that the most recent collection item response contains the expected name and originalUrl."""
    try:
        body = context.last_response.json()
    except Exception:
        raise AssertionError("Response does not contain valid JSON to assert collection item attributes")
    attributes = None
    if isinstance(body, dict):
        data_section = body.get('data')
        # Single item response
        if isinstance(data_section, dict):
            attributes = data_section.get('attributes', {})
        # List of items (e.g. get_collection_for_collection)
        elif isinstance(data_section, list):
            for item in data_section:
                if str(item.get('id')) == str(getattr(context, 'collection_item_id', None)):
                    attributes = item.get('attributes', {})
                    break
    if not attributes:
        raise AssertionError("No attributes found in response to assert collection item name and original url")
    actual_name = attributes.get('name')
    actual_original_url = attributes.get('originalUrl')
    assert actual_name == name, f"Expected collection item name '{name}' but got '{actual_name}'"
    assert actual_original_url == original_url, f"Expected collection item originalUrl '{original_url}' but got '{actual_original_url}'"


@then('the collection description should be "{description}" and status should be "{status}"')
def step_assert_collection_description_status(context, description, status):
    """Assert that the most recent collection response contains the expected description and status."""
    try:
        body = context.last_response.json()
    except Exception:
        raise AssertionError("Response does not contain valid JSON to assert collection description and status")
    attributes = None
    if isinstance(body, dict):
        data_section = body.get('data')
        if isinstance(data_section, dict):
            attributes = data_section.get('attributes', {})
    if not attributes:
        raise AssertionError("No attributes found in response to assert collection description and status")
    actual_description = attributes.get('description')
    actual_status = attributes.get('status')
    assert actual_description == description, f"Expected collection description '{description}' but got '{actual_description}'"
    assert actual_status == status, f"Expected collection status '{status}' but got '{actual_status}'"


@when('the user attempts to retrieve the collection item')
def step_attempt_get_collection_item(context):
    """Attempt to retrieve a previously deleted collection item and store the response."""
    response = get_collection_item(context.collection_item_id)
    context.last_response = response


@when('the user attempts to retrieve the collection')
def step_attempt_get_collection(context):
    """Attempt to retrieve a previously deleted collection and store the response.

    Because ``coll.py`` does not expose a direct get‑by‑id function for collections,
    we call ``get_collection_for_collection`` which is expected to return
    404 once the parent collection no longer exists.
    """
    response = get_collection_for_collection(context.collection_id)
    context.last_response = response


@when('the user retrieves items for the collection')
def step_get_items_for_collection(context):
    """Retrieve the items associated with the stored collection ID."""
    response = get_collection_for_collection(context.collection_id)
    context.last_response = response


@then('the collection item id should be present in the response')
def step_assert_collection_item_in_response(context):
    """Verify that the saved collection item ID appears in the items list."""
    try:
        body = context.last_response.json()
    except Exception:
        raise AssertionError("Response does not contain valid JSON from which to verify presence of collection item ID")
    data_section = body.get('data', [])
    ids = []
    if isinstance(data_section, list):
        for item in data_section:
            ids.append(str(item.get('id')))
    elif isinstance(data_section, dict):
        ids.append(str(data_section.get('id')))
    found = str(context.collection_item_id) in ids
    assert found, f"Collection item ID {context.collection_item_id} not found in response data {ids}"


@when('the user retrieves the collection item')
def step_get_collection_item(context):
    """Retrieve a specific collection item by its ID."""
    response = get_collection_item(context.collection_item_id)
    context.last_response = response


@when('the user deletes the collection item')
def step_delete_collection_item(context):
    """Delete a specific collection item."""
    response = delete_collection_item(context.collection_item_id)
    context.last_response = response


@when('the user deletes the collection')
def step_delete_collection(context):
    """Delete the previously created collection."""
    response = delete_collection(context.collection_id)
    context.last_response = response


@then('the collection item id should match saved id and name should be "{name}" and original url should be "{original_url}"')
def step_assert_collection_item_details(context, name, original_url):
    """Assert that a single collection item response contains the expected id, name and originalUrl."""
    try:
        body = context.last_response.json()
    except Exception:
        raise AssertionError("Response does not contain valid JSON to assert collection item details")
    # Expect a single item structure
    if not isinstance(body, dict) or 'data' not in body or not isinstance(body['data'], dict):
        raise AssertionError("Unexpected structure for collection item details response")
    data_section = body['data']
    returned_id = str(data_section.get('id'))
    attributes = data_section.get('attributes', {})
    actual_name = attributes.get('name')
    actual_original_url = attributes.get('originalUrl')
    assert returned_id == str(context.collection_item_id), (
        f"Expected collection item id '{context.collection_item_id}' but got '{returned_id}'"
    )
    assert actual_name == name, f"Expected collection item name '{name}' but got '{actual_name}'"
    assert actual_original_url == original_url, (
        f"Expected collection item originalUrl '{original_url}' but got '{actual_original_url}'"
    )