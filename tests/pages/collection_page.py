import re
from pathlib import Path

from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage

class CollectionPage(BasePage):
    #CREATOR INFO
    EDIT_CREATOR_INFO_BUTTON = (By.XPATH, "//button[@class='baseButton baseButton--primary baseButton--small baseButton--iconleft collectionsList__creatorInfoButton']")
    AVATAR_IMG = (By.XPATH, "//img[@class='baseImage  collectionsList__creatorInfoAvatar']")
    CREATOR_NAME = (By.XPATH, "//h3[@class='collectionsList__creatorInfoName']")
    #TOP TABS
    PUBLISHED_TAB_BUTTON = (By.XPATH, "//button[.='Published']")
    DRAFTS_TAB_BUTTON = (By.XPATH, "//button[.='Drafts']")
    ARCHIVED_TAB_BUTTON = (By.XPATH, "//button[.='Archived']")
    NEW_COLLECTION_BUTTON = (By.XPATH, "//button[contains(@class, 'collectionsList__controlsButton--newCollection')]")
    #PUBLISHED COLLECTIONS
    COLLECTION_IMG = (By.XPATH, "//img[@class='baseImage  collectionsListCard__image']")
    FIRST_COLLECTION_IMG = (By.XPATH, "(//img[@class='baseImage  collectionsListCard__image'])[1]")
    COLLECTION_NAME = (By.XPATH, "//span[@class='collectionsListCard__name']")
    FIRST_COLLECTION_NAME = (By.XPATH, "(//span[@class='collectionsListCard__name'])[1]")
    COLLECTION_EDIT_BTN = (By.XPATH, "//button[.='Edit']")
    FIRST_COLLECTION_EDIT_BTN = (By.XPATH, "(//button[.='Edit'])[1]")
    COLLECTION_VIEW_BTN = (By.XPATH, "//a[contains(@class, 'collectionsListCard__actionsButton--view')]")
    COLLECTION_COPY_BTN = (By.XPATH, "//button[@class='collectionsListCard__actionsButton--copy']")
    #ADD A NEW COLLECTION
    COLLECTION_NAME_INPUT = (By.XPATH, "//input[@class='baseInputField__input']")
    COLLECTION_NAME_CHECKER = (By.XPATH, "//li[@class='formValidationList__listItem formValidationList__listItem--valid']")
    CREATE_BTN = (By.XPATH, "//button[contains(@class, 'collectionsAdd__sideActionsButton--draft')]")
    #EDIT COLLECTION
    BROWSE_FILE = (By.XPATH, "//button[contains(@class, 'imageUploadField__dropzonePromptButton')]")
    HERO_IMAGE_UPLOAD = (By.XPATH, "//input[@class='imageUploadField__hiddenInput']")
    COLLECTION_DESCRIPTION = (By.XPATH, "//textarea[@id='input-description']")
    SET_NAME_CHECKER = (By.XPATH, "(//li[@class='collectionSetupGuide__listItem collectionSetupGuide__listItem--complete'])[1]")
    UPLOAD_HERO_IMG_CHECKER = (By.XPATH, "(//li[@class='collectionSetupGuide__listItem collectionSetupGuide__listItem--complete'])[2]")
    ADD_ITEM_CHECKER = (By.XPATH, "(//span[@class='baseIcon collectionSetupGuide__listItemIcon'])[3]")
    PUBLISH_COLLECTION_BTN = (By.XPATH, "//button[contains(@class, '--publish')]")
    UPDATE_COLLECTION_BTN = (By.XPATH, "//button[contains(@class, '--update')]")
    VIEW_COLLECTION_BTN = (By.XPATH, "//button[contains(@class, '--view')]")
    MOVE_TO_DRAFT_COLLECTION_BTN = (By.XPATH, "//button[@class='collectionsEdit__sideActionsButton--moveToDraft']")
    ARCHIVE_COLLECTION_BTN = (By.XPATH, "//button[@class='collectionsEdit__sideActionsButton--moveToArchive']")
    DELETE_COLLECTION_BTN = (By.XPATH, "//button[@class='collectionsEdit__sideActionsButton--delete']")
    #ITEMS
    DESTINATION_URL_INPUT = (By.XPATH, "//input[@id='productInfoFormItemUrl']")
    MONETIZE_BTN_COLLECTION = (By.XPATH, "//input[@class='baseToggle__input']")
    ADD_ITEM_BTN_COLLECTION = (By.XPATH, "//button[@class='productInfoForm__formButton']")
    ITEM_NAME_INPUT = (By.XPATH, "//input[@id='addItemName']")
    ITEM_IMG_BROWSE_FILE_BTN = (By.XPATH, "//button[@class='imageUploadField__dropzonePromptButton']")
    STORE = (By.XPATH, "//input[@class='addItemStore']")
    ADD_ITEM_BTN_ITEM = (By.XPATH, "//button[@class='baseButton baseButton--primary baseButton--small']")
    UPDATE_ITEM_POPUP_BTN = (By.XPATH, "//button[@class='baseButton baseButton--primary baseButton--small']")
    REORDER_ITEMS_BTN = (By.XPATH, "//button[.='Reorder Products']")
    SAVE_REORDER_BTN = (By.XPATH, "//button[.='Save Re-order']")
    REORDER_CANCEL_BTN = (By.XPATH, "//button[.='Cancel']")
    ITEM_1 = (By.XPATH, "//input[@class='collectionsItem  collectionsItem--minified']")
    ITEM_EDIT_BTN_1 = (By.XPATH, "(//button[.='Edit'])[1]")
    ITEM_REMOVE_BTN_1 = (By.XPATH, "(//button[.='Remove'])[1]")
    ITEM_IMAGE_UPLOAD = (By.XPATH, "//div[@class='popUp__card']//input[@class='imageUploadField__hiddenInput']")
    #SHOPPERS PAGE
    SHOPPER_COLLECTION_NAME = (By.XPATH, "//h1[@class='collectionHeader__profileInnerInfoTitle']")
    SHOPPER_ITEM_CARDS = (By.XPATH, "//li[@class='collectionList__item']")
    SHOPPER_HERO_IMG = (By.XPATH, "//img[@class='collectionHero__image']")
    SHOPPER_CREATOR_NAME = (By.XPATH, "//p[@class='collectionHeader__profileInnerInfoHandle']")
    SHOPPER_AVATAR_IMG = (By.XPATH, "//img[@class='collectionHeader__profileInnerAvatar']")
    SHOPPER_ITEM_IMG = (By.XPATH, "//img[@class='collectionItem__imageTag']")
    SHOPPER_ITEM_NAME = (By.XPATH, "//h3[@class='collectionItem__contentTitle']")
    SHOPPER_ITEM_STORE = (By.XPATH, "//span[@class='collectionItem__contentStoreName']")
    SHOPPER_ITEM_VIEW_PRODUCT_BTN = (By.XPATH, "//button[.='View Product']")
    ADMIN_ITEM_CARD = (By.CSS_SELECTOR, "li.collectionsItemsList__item, li.collectionList__item")
    ADMIN_ITEM_NAME = (By.CSS_SELECTOR, "h3.collectionItemCard__title, h3.collectionItem__contentTitle")

    # --- Properties: Creator info ---

    @property
    def edit_creator_info_button(self):
        return self.element(self.EDIT_CREATOR_INFO_BUTTON)

    @property
    def avatar_img(self):
        return self.element(self.AVATAR_IMG)

    @property
    def creator_name(self):
        return self.element(self.CREATOR_NAME)

    # --- Properties: Top tabs / actions ---

    @property
    def published_tab_button(self):
        return self.element(self.PUBLISHED_TAB_BUTTON)

    @property
    def drafts_tab_button(self):
        return self.element(self.DRAFTS_TAB_BUTTON)

    @property
    def archived_tab_button(self):
        return self.element(self.ARCHIVED_TAB_BUTTON)

    @property
    def new_collection_button(self):
        return self.element(self.NEW_COLLECTION_BUTTON)

    # --- Properties: Collections list (cards) ---

    @property
    def collection_img(self):
        return self.element(self.COLLECTION_IMG)

    @property
    def first_collection_img(self):
        return self.element(self.FIRST_COLLECTION_IMG)

    @property
    def collection_name(self):
        return self.element(self.COLLECTION_NAME)

    @property
    def first_collection_name(self):
        return self.element(self.FIRST_COLLECTION_NAME)

    @property
    def collection_edit_btn(self):
        return self.element(self.COLLECTION_EDIT_BTN)

    @property
    def first_collection_edit_btn(self):
        return self.element(self.FIRST_COLLECTION_EDIT_BTN)

    @property
    def collection_view_btn(self):
        return self.element(self.COLLECTION_VIEW_BTN)

    @property
    def collection_copy_btn(self):
        return self.element(self.COLLECTION_COPY_BTN)

    @property
    def collection_cards(self):
        """Return all collection cards' WebElements (images/names)."""
        return self.elements(self.COLLECTION_NAME)

    # --- Properties: New collection panel ---

    @property
    def collection_name_input(self):
        return self.element(self.COLLECTION_NAME_INPUT)

    @property
    def collection_name_checker(self):
        return self.element(self.COLLECTION_NAME_CHECKER)
    @property
    def create_btn(self):
        return self.element(self.CREATE_BTN)

    # --- Properties: Edit collection (details + side actions) ---

    @property
    def browse_file(self):
        return self.element(self.BROWSE_FILE)

    @property
    def hero_img_upload(self):
        return self.element(self.HERO_IMAGE_UPLOAD)

    @property
    def collection_description(self):
        return self.element(self.COLLECTION_DESCRIPTION)

    @property
    def set_name_checker(self):
        return self.element(self.SET_NAME_CHECKER)

    @property
    def upload_hero_img_checker(self):
        return self.element(self.UPLOAD_HERO_IMG_CHECKER)

    @property
    def add_item_checker(self):
        return self.element(self.ADD_ITEM_CHECKER)

    @property
    def publish_collection_btn(self):
        return self.element(self.PUBLISH_COLLECTION_BTN)

    @property
    def update_collection_btn(self):
        return self.element(self.UPDATE_COLLECTION_BTN)

    @property
    def view_collection_btn(self):
        return self.element(self.VIEW_COLLECTION_BTN)

    @property
    def move_to_draft_collection_btn(self):
        return self.element(self.MOVE_TO_DRAFT_COLLECTION_BTN)

    @property
    def archive_collection_btn(self):
        return self.element(self.ARCHIVE_COLLECTION_BTN)

    @property
    def delete_collection_btn(self):
        return self.element(self.DELETE_COLLECTION_BTN)

    # --- Properties: Items inside collection (edit view) ---

    @property
    def destination_url_input(self):
        return self.element(self.DESTINATION_URL_INPUT)

    @property
    def monetize_btn_collection(self):
        return self.element(self.MONETIZE_BTN_COLLECTION)

    @property
    def add_item_btn_collection(self):
        return self.element(self.ADD_ITEM_BTN_COLLECTION)

    @property
    def item_name_input(self):
        return self.element(self.ITEM_NAME_INPUT)

    @property
    def item_img_browse_file_btn(self):
        return self.element(self.ITEM_IMG_BROWSE_FILE_BTN)

    @property
    def store_input(self):
        return self.element(self.STORE)

    @property
    def add_item_btn_item(self):
        return self.element(self.ADD_ITEM_BTN_ITEM)

    @property
    def update_item_popup_btn(self):
        return self.element(self.UPDATE_ITEM_POPUP_BTN)

    @property
    def reorder_items_btn(self):
        return self.element(self.REORDER_ITEMS_BTN)

    @property
    def save_reorder_btn(self):
        return self.element(self.SAVE_REORDER_BTN)

    @property
    def reorder_cancel_btn(self):
        return self.element(self.REORDER_CANCEL_BTN)

    @property
    def item_1(self):
        return self.element(self.ITEM_1)

    @property
    def item_edit_btn_1(self):
        return self.element(self.ITEM_EDIT_BTN_1)

    @property
    def item_remove_btn_1(self):
        return self.element(self.ITEM_REMOVE_BTN_1)

    @property
    def item_image_upload(self):
        return self.element(self.ITEM_IMAGE_UPLOAD)

    # --- Properties: Shopper (public) collection page ---

    @property
    def shopper_collection_name(self):
        return self.element(self.SHOPPER_COLLECTION_NAME)

    @property
    def shopper_item_cards(self):
        return self.elements(self.SHOPPER_ITEM_CARDS)

    @property
    def shopper_hero_img(self):
        return self.element(self.SHOPPER_HERO_IMG)

    @property
    def shopper_creator_name(self):
        return self.element(self.SHOPPER_CREATOR_NAME)

    @property
    def shopper_avatar_img(self):
        return self.element(self.SHOPPER_AVATAR_IMG)

    @property
    def shopper_item_img(self):
        return self.elements(self.SHOPPER_ITEM_IMG)

    @property
    def shopper_item_name(self):
        return self.elements(self.SHOPPER_ITEM_NAME)

    @property
    def shopper_item_store(self):
        return self.elements(self.SHOPPER_ITEM_STORE)

    @property
    def shopper_item_view_product_btn(self):
        return self.elements(self.SHOPPER_ITEM_VIEW_PRODUCT_BTN)

    @property
    def admin_item_cards(self):
        return self.elements(self.ADMIN_ITEM_CARD)

    @property
    def admin_item_names(self):
        return self.elements(self.ADMIN_ITEM_NAME)

    # -------------------------------------------------------------------------
    # Custom helper methods for Collections UI flows
    # -------------------------------------------------------------------------

    def upload_img(self, filename: str):
        # Build absolute path to file inside your test project / container
        project_root = Path(__file__).resolve().parents[2]
        img_path = project_root / "tests" / "utilities" / "test_data" / filename

        assert img_path.exists(), f"Image file not found: {img_path}"

        # (Optional) click the button so the UI state is consistent
        #self.browse_file.click()

        #send the absolute path to the hero_image_upload
        file_input = self.hero_img_upload.webelement
        file_input.send_keys(str(img_path))


    def switch_tab(self, tab: str):
        """
        Switch between Published / Drafts / Archived tabs using a string key.
        Example: switch_tab("published"), switch_tab("drafts"), switch_tab("archived")
        """
        tab = (tab or "").strip().lower()
        mapping = {
            "published": self.published_tab_button,
            "drafts": self.drafts_tab_button,
            "archived": self.archived_tab_button,
        }
        if tab not in mapping:
            raise ValueError(f"Unknown tab '{tab}'. Expected one of {list(mapping.keys())}")
        mapping[tab].click()

    def start_new_collection(self, name: str):
        """
        Click 'New Collection', type name, and click 'Create' to create a draft collection.

        Returns: None – but you can follow with other calls (e.g. set_description, add_item, publish).
        """
        self.new_collection_button.click()
        self.collection_name_input.clear_all()
        self.collection_name_input.type(name)
        self.create_collection_btn.click()

    def set_description(self, description: str):
        """
        Set the collection description in the edit view.
        """
        self.collection_description.clear_all()
        self.collection_description.type(description)

    def is_setup_checklist_complete(self) -> bool:
        """
        Returns True if all three setup guide checkmarks (name, hero image, item) are visible.
        """
        checks = [
            self.set_name_checker,
            self.upload_hero_img_checker,
            self.add_item_checker,
        ]
        return all(c.is_visible() for c in checks)

    def add_item(
            self,
            destination_url: str,
            name: str | None = None,
            store: str | None = None,
            monetize: bool | None = None,
    ):
        """
        Fill in the item form and click the primary add button.

        This is deliberately minimal – assertions about the result (item appears in list,
        shopper view shows it, etc.) should live in your steps.
        """
        self.destination_url_input.clear_all()
        self.destination_url_input.type(destination_url)

        if monetize is not None:
            # baseToggle__input is a checkbox; Element.get_attribute used to inspect state
            is_checked = self.monetize_btn_collection.get_attribute("checked") is not None
            if monetize != is_checked:
                self.monetize_btn_collection.click()

        if name is not None:
            self.item_name_input.clear_all()
            self.item_name_input.type(name)

        if store is not None:
            self.store_input.clear_all()
            self.store_input.type(store)

        # Depending on UX, either the form button or the small primary button will exist.
        try:
            self.add_item_btn_collection.click()
        except Exception:
            self.add_item_btn_item.click()

    def open_collection_from_list(self, index: int = 1, action: str = "edit"):
        """
        From the collections list, click Edit/View on the Nth card.

        :param index: 1-based index of the collection card in current tab.
        :param action: 'edit' or 'view'
        """
        action = (action or "").strip().lower()
        if action not in {"edit", "view"}:
            raise ValueError("action must be 'edit' or 'view'")

        locator = self.COLLECTION_EDIT_BTN if action == "edit" else self.COLLECTION_VIEW_BTN
        buttons = self.elements(locator)
        if not buttons:
            raise AssertionError(f"No collection {action} buttons found on the page")

        idx = max(0, index - 1)
        if idx >= len(buttons):
            raise IndexError(f"Requested index {index} but only {len(buttons)} collections present")
        buttons[idx].click()

    def get_shopper_item_texts(self):
        """
        Convenience helper for shopper page:
        Returns a list of dicts [{name: ..., store: ...}, ...] for visible items.
        """
        names = [el.text for el in self.elements(self.SHOPPER_ITEM_NAME)]
        stores = [el.text for el in self.elements(self.SHOPPER_ITEM_STORE)]
        items = []
        for i, name in enumerate(names):
            store = stores[i] if i < len(stores) else ""
            items.append({"name": name, "store": store})
        return items

    def get_item_names_any_view(self):
        """Return visible item names from either admin or shopper views."""
        names = []
        try:
            names = [el.text for el in self.admin_item_names if el.text]
        except Exception:
            pass

        if not names:
            try:
                names = [el.text for el in self.elements(self.SHOPPER_ITEM_NAME) if el.text]
            except Exception:
                pass

        if not names:
            try:
                pattern = re.compile(r"Collection Item[^<]*:([^<\\n]+)")
                names = pattern.findall(self.driver.page_source)
            except Exception:
                names = []
        return names