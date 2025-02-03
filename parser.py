from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


class Parser:
    def __init__(self) -> None:
        self.data = []
        self.selectors = {
            'button_apartments': '//*[@id="heading1"]/h5/button',
            'button_private_houses': '//*[@id="heading2"]/h5/button',
            'table_apartments_internet': '//*[@id="collapse1"]/div/table[1]',
            'table_apartments_combo': '//*[@id="collapse1"]/div/table[2]',
            'table_private_houses_internet': '//*[@id="collapse2"]/div/table[1]',
            'table_private_houses_combo': '//*[@id="collapse2"]/div/table[2]',
        }
        self.url = 'https://www.rialcom.ru/internet_tariffs/'
        self.service = Service(executable_path='./chromedriver')
        self.options = Options()
        self.options.add_argument('--headless')
        # self.options.add_experimental_option('detach', True)
        # self.options.add_argument(f'--proxy-server={proxy_server_ip}')
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def open_page(self, url: str) -> None:
        self.driver.get(url)

    def __parse_internet(self, table_xpath: str) -> None:
        table = self.driver.find_element(By.XPATH, table_xpath)
        for i, row in enumerate(table.find_elements(By.XPATH, './tbody/tr')):
            tariff_name = row.find_element(By.XPATH, './td[1]').text
            sub_fee = row.find_element(By.XPATH, './td[2]').text
            sub_fee = int(re.sub(r'\D', '', sub_fee))
            speed = row.find_element(By.XPATH, './td[4]').text
            speed = int(re.sub(r'\D', '', speed)) / 1000
            # print(tariff_name, sub_fee, speed, sep=' | ')
            self.data.append({
                'Название тарифа': tariff_name,
                'Количество каналов': None,
                'Скорость доступа': speed,
                'Абонентская плата': sub_fee
            })

    def __parse_combo(self, table_xpath: str) -> None:
        table = self.driver.find_element(By.XPATH, table_xpath)
        header_tariff = table.find_elements(By.XPATH, ".//thead/tr/th[position()>1]")
        for idx, tariff in enumerate(header_tariff):
            speed = int(re.search(r'\d+', tariff.text).group())
            for row in table.find_elements(By.XPATH, './tbody/tr'):
                channel_pattern = r'\s\((\d+)\s\w+\)'
                tariff_name = row.find_element(By.XPATH, './td[1]').text + ' + ' + tariff.text
                match = re.search(channel_pattern, tariff_name)
                if match:
                    channels = int(match.group(1))
                else:
                    channels = None
                tariff_name = re.sub(channel_pattern, '', tariff_name)
                sub_fee = row.find_element(By.XPATH, f'./td[{idx + 2}]').text
                sub_fee = int(re.sub(r'\D', '', sub_fee))
                # print(tariff_name, channels, speed, sub_fee, sep=' | ')
                self.data.append({
                    'Название тарифа': tariff_name,
                    'Количество каналов': channels,
                    'Скорость доступа': speed,
                    'Абонентская плата': sub_fee
                })

    def parse_apartments(self) -> None:
        self.driver.find_element(By.XPATH, self.selectors['button_apartments']).click()
        WebDriverWait(
            self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.selectors['table_apartments_internet'])))
        self.__parse_internet(self.selectors['table_apartments_internet'])
        self.__parse_combo(self.selectors['table_apartments_combo'])

    def parse_private_houses(self) -> None:
        self.driver.find_element(By.XPATH, self.selectors['button_private_houses']).click()
        WebDriverWait(
            self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.selectors['table_private_houses_internet'])))
        self.__parse_internet(self.selectors['table_private_houses_internet'])
        self.__parse_combo(self.selectors['table_private_houses_combo'])

    def close_browser(self) -> None:
        # print(len(self.data))
        self.driver.quit()