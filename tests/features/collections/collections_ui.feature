# This feature tests the full life‑cycle of a collection and its items
# It covers a full regression scenario that covers creation, update, retrieval and deletion of both
# collections and collection items.
@collection_ui @ui
Feature: Collection UI (Collections + Collection Items)
  As a Creator I want to create a Collection with Collection Items and publish, update, and delete it.

  Background: User is on Collection page
    Given user logs in as a "user"
    Given user navigates to the "collections" page

  @collection_ui @ui
  Scenario: Create a Draft, Update the Draft, Publish the Collection,Visit the Collection, Archive the Collection and Delete the Collection
    #Navigating to Collection edit
  Then user should see Collection Header, Creator info
  Then user should see 'Published', 'Draft' and 'Archive' tab buttons, and 'New Collection' button
  Then user should see a published Collection named 'Collection Test', it's image, 'Edit', 'View' and 'Url Copy' buttons

     #Create a Draft Collection and Update
  When user clicks on 'New Collection'
  And user enters "Test Automation Collection" in Collection name field
  Then user should see "Collection Name" crossed out and got green check mark in Summary
  When user clicks on "Create" button
  And user uploads Collection Hero image
  And user enters 'This is a Collection Test' Collection Description and store Collection's url.
  And user clicks on 'Update' button
  Then user clicks on 'Draft' button and assert 'Test Automation Collection' in collection names
  And user stores Hero images uuid, avatar images uuid

    #Add 3 couple Items
  When user clicks on 'Edit' button of the collection created
  And user scroll down to 'Add a new item to this Collection' and adds items with following Kohl's Url in Destination Url
    |https://www.kohls.com/product/prd-4544860/shark-pet-cordless-stick-vacuum-ix141.jsp|
    |https://www.kohls.com/product/prd-5026580/monarch-cupholder-end-table.jsp?color=Taupe|
  And user clicks on 'Monetize this link' button
  And user clicks on 'Add a new item to this Collection' and enters Kohl's Url in Destination Url
      |https://www.kohls.com/product/prd-6602194/sonoma-goods-for-life-ultimate-hygrocotton-sheet-set-with-pillowcases.jsp?color=Light%20Gray|
  Then user should see three items in the Collection Items with following names
    |Sonoma Goods For Life® Ultimate HygroCotton® Sheet Set with Pillowcases, Ivory|
    |Monarch Cupholder End Table, Brown|
    |Shark® Pet Cordless Stick Vacuum IX141, Blue|
  Then user should see two affiliate link and one Kohl's url in affiliate link button

    #Update the Draft / Item
  When user clicks on "Edit" button on second from the top Collection Item
  And updates Item names to "Monarch Cupholder End Table, Brown UPDATED" and Store to Kohl's UPDATED
  And clicks on Update Item
  Then User should see 'UPDATED' in Collection name and Store
  And user stores item images uuid

    #Change the order of Items
  When user clicks on 'Reorder Product'
  And user drags the top item to the bottom
  And user clicks on 'Save Reorder' button
  Then user should see top item with 'UPDATE' in it's name

    #Delete the Item
  When user clicks on 'Remove' button of top item
  And user clicks on 'Remove Item' button on pop up
  Then user should see only two items
  And user should not see 'Monarch Cupholder End Table, Brown UPDATED" and Store to Kohl's UPDATED' in item names

    #Preview the Collection
  When user clicks on 'Preview' button
  Then user should navigate to the url that has /preview in it
  When user clicks on 'View' button
  Then user should see the collection with the name of 'Test Automation Collection' in a new tab
  Then user should see the two collection items
  Then user should see the Hero image and Description
  Then user should see Creators info and avatar image and goes back to Collection Admin page
  When user stores Shopper page's url

    #Publish the Collection
  Then user should see 'Set Name', 'Upload a hero image', 'Add at least 1 item' crossed out and got a green check marks
  When user clicks on 'Publish' button on Collection edit page
  Then user should see 'Test Automation Collection' in the published tab

    #Visit the Collection
  When user clicks on 'View' button
  Then user should see the collection with the name of 'Test Automation Collection' in a new tab
  Then user should see the two collection items
  Then user should see item's img, store, name, and view product button.
  When user clicks on 'view product' button
  Then user should see 'https://www.kohls.com/product/prd-4544860/shark-pet-cordless-stick-vacuum-ix141.jsp' in url
  Then user should see the Hero image and Description
  Then user should see Creators info and avatar image and goes back to Collection Admin page
  When user stores Shopper page's url
  When user goes back to Collection Admin page and copies the Collection's Url
  Then Collection's url matches with published collection's url

    #Archive the Collection
  When user clicks on 'Edit' button on the collection
  And user clicks on 'Archive' button
  When user clicks on 'Archive' tab
  Then user should see the Collection with the name 'Test Automation Collection'

    #Delete the Collection
  When user clicks on 'Edit' button on 'Test Automation Collection' collection
  And user clicks on 'Delete' button
  And user clicks on 'Delete Collection' button on pop up
  And user clicks on 'Archive' tab
  Then user should not see the 'Test Automation Collection' Collection in Archive tab
  And user should get 404 following the Collection's url
