from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import time
import base64
import json
from datetime import datetime
from random import randint
from fake_useragent import UserAgent


class googleImg:
    def __init__(self):
        '''執行webdriver，檢查chromedriver.exe是否存在另確認版本是否可用'''
        '''建立webdeiver物件，並禁止彈出式視窗'''
        self.__chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        self.__chrome_options.add_experimental_option("prefs", prefs)
        '''背景執行'''
        self.__chrome_options.add_argument("--headless")

    def download(self, mainKwd, otherKwds: list):
        for kwd in otherKwds:
            img_src = self.__allUrl(f"{mainKwd}+{kwd}")
            self.__saveAll(f"{mainKwd}_{kwd}", img_src)

    def __allUrl(self, searchKwd) -> list:
        url = f'https://www.google.com/search?q={searchKwd}&tbm=isch&oq={searchKwd}&sclient=img'

        # url = f'https://www.google.com/search?q={"+".join(kwd)}&tbm=isch&ved=2ahUKEwj18pGavJr0AhUUBN4KHQXoDK8Q2-cCegQIABAA&oq={"+".join(kwd)}'\
        #     '&gs_lcp=CgNpbWcQDDIHCCMQ7wMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgARQAFgAYIwFaABwAHgAgAFSiAFSkgEBMZgBAKoBC2d3cy13aXotaW1nwAEB'\
        #     '&sclient=img&ei=IGCSYfXiEJSI-AaF0LP4Cg&bih=714&biw=1536'

        # url = https: // www.google.com/search?q = %E9 % AB % 98 % E9 % BA % 97 % E8 % 8F % 9C & sclient = img & tbm = isch
        driver = webdriver.Chrome(chrome_options=self.__chrome_options)

        driver.get(url)
        time.sleep(2+randint(10, 20)/10)
        for i in range(10):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            try:
                # driver.find_element_by_css_selector('input.mye4qd').click()
                driver.find_element(By.CSS_SELECTOR, 'input.mye4qd').click()
            except:
                pass

            try:
                # print(driver.find_element_by_css_selector(
                #     'div.OuJzKb.Yu2Dnd > div').text == "")
                if driver.find_element(By.CSS_SELECTOR, 'div.OuJzKb.Yu2Dnd > div').text != "":
                    break
            except:
                pass
            time.sleep(1+randint(2, 5)/10)

        bs = BeautifulSoup(driver.page_source, "html5lib")
        # with open('test.html', 'w', encoding='utf-8') as f:
        #     f.write(self.__driver.page_source)
        driver.quit()

        img_src = []
        n = 1
        temp = bs.find_all("img")
        for i in temp:
            print(f'\r{searchKwd} {n:>3}/{len(temp)}', end='')
            n += 1
            try:
                img_str = i['src']
                img_src.append(img_str)
            except:
                try:
                    headers = {
                        "user-agent": UserAgent().random
                    }
                    res = requests.get(i['data-src'], headers=headers)
                    img_src.append(res.content)
                    time.sleep(randint(7, 12)/10)
                except:
                    pass

        return img_src

    def __saveAll(self, folder: str, img_src: list):
        fileTime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        file_path = Path(f'./{folder}_{fileTime}')
        if not(file_path.exists()):
            file_path.mkdir()  # 建立目錄， parents 參數若是 True, 形同 mkdirs

        i = 1
        err = []
        print()
        for img_str in img_src:
            print(f'\r{i:>3}/{len(img_src)}', end='')
            if str(img_str).startswith("data:image/jpeg;base64,"):
                try:
                    img_str = img_str.replace("data:image/jpeg;base64,", "")
                    img_data = base64.b64decode(img_str)
                    with open(f'{file_path}/{i}.jpg', 'wb') as f:
                        f.write(img_data)
                    i += 1
                except:
                    err.append(img_str)
            elif str(img_str).startswith("https://encrypted"):
                headers = {
                    "user-agent": UserAgent().random
                }
                try:
                    res = requests.get(str(img_str), headers=headers)
                    with open(f'{file_path}/{i}.jpg', 'wb') as f:
                        f.write(res.content)
                    i += 1
                except:
                    err.append(img_str)
                time.sleep(randint(7, 12)/10)
            else:
                try:
                    with open(f'{file_path}/{i}.jpg', 'wb') as f:
                        f.write(img_str)
                    i += 1
                except:
                    err.append(img_str)

        if err != []:
            try:
                with open(f'./err/err_{fileTime}.txt', 'wa', encoding='utf-8') as f:
                    f.write('{}'.format("\n\n".join(err)))
            except:
                pass


def main(*otherKwds):
    s = time.time()
    with open("food_kind.json", 'r', encoding='utf-8') as f:
        temp = f.read()
    fk = json.loads(temp)
    for k, vs in fk.items():
        for v in vs:
            gi = googleImg()
            gi.download(v, otherKwds)

    fileTime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    for k, vs in fk.items():
        file_path = Path(f'./{k}_{fileTime}')
        if not(file_path.exists()):
            file_path.mkdir()  # 建立目錄， parents 參數若是 True, 形同 mkdirs
        for v in vs:
            for i in Path('./').iterdir():
                if i.is_dir() and str(i).startswith(v):
                    oriPath = Path(f'./{i}')
                    tarPath = Path(f'{file_path}/{i}')
                    oriPath.replace(tarPath)
    e = time.time()

    hh = (e-s)//3600
    ss = (e-s) % 60
    mm = ((e-s)-ss-hh*3600)//60
    print(e-s)
    print(f'共花費{hh}小時{mm}分{ss}秒')


if __name__ == '__main__':
    main("food", "ingredients", "cook")
