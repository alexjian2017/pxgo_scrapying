import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from prettytable import PrettyTable
import pxgo.constant as const
from datetime import datetime


class Pxgo(webdriver.Chrome):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disk-cache-size=1")
        chrome_options.add_argument("--media-cache-size=1")
        chrome_options.add_argument("--disable-application-cache")
        chrome_options.add_argument("--disable-cache")
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        # inheritance
        super(Pxgo, self).__init__(
            chrome_options=chrome_options)
        # 預設等待網頁回應時間，如果已經有回應就會繼續下一步
        self.implicitly_wait(15)
        # 使視窗最大化
        self.maximize_window()

    def test(self):
        self.get('https://httpbin.org/headers')  # 使用測試網站 httpbin.org/headers

        # 等待網頁載入完成
        self.implicitly_wait(10)

        # 取得網頁內容
        page_source = self.page_source

        # 顯示網頁內容，檢查是否含有自定義 User Agent 標頭
        print(page_source)

    def get_date(self) -> str:
        return datetime.now().strftime('%Y-%m-%d')

    def get_first_page(self):
        self.get(const.BASE_URL)

    def get_certain_category(self, category: str = '蔬菜水果'):
        menu_names = self.find_elements(By.CLASS_NAME, 'custom-menu-text')
        # # xpath 寫法
        # menu_names = self.find_elements(By.XPATH, '//div[@class="custom-menu-text"]')
        for menu_name in menu_names:
            inner_html = self.execute_script(
                'return arguments[0].innerHTML;', menu_name)
            if inner_html.strip() == category:
                # 執行您需要的處理，例如點擊該元素、取得其他資訊等
                menu_name.click()
                break

    def get_second_page(self):
        # 選擇第一個出現的menu分類，進入下一個動態網頁
        menu_name = self.find_element(By.CLASS_NAME, 'custom-menu-text')
        menu_name.click()

    def small_category(self, category_name: str, db, date: str):
        right_section = self.find_element(By.CLASS_NAME, 'right-div')
        right_section.click()
        actions = ActionChains(self)
        while 1:
            for _ in range(5):
                actions.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(5)  # 等待一段時間，讓網頁載入更多內容
            loading_word = self.find_element(
                By.CLASS_NAME, 'mescroll-upwarp').get_attribute('innerHTML').strip()
            if len(loading_word) == 0:
                break
        items = self.find_elements(By.CLASS_NAME, 'falls-normal')
        for item in items:
            price = item.find_element(
                By.CLASS_NAME, 'share-way-suggest').get_attribute('innerHTML').strip()
            price = price.split()[0]
            name, w = item.find_element(
                By.CLASS_NAME, 'falls-font').get_attribute('innerHTML').strip().split()

            db.insert_data(name, w, price, date)

    def large_category(self, category_id: str, db, date: str):
        l_category_element = self.find_element(By.ID, category_id)
        l_category_element.click()

        s_categories_elements = self.find_elements(
            By.CLASS_NAME, 'left-div-list-children-item')
        for s_category in s_categories_elements:
            category_name = s_category.get_attribute('innerHTML').strip()
            s_category.click()
            self.small_category(category_name, db, date)
