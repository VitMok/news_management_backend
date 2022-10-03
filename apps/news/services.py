import time

from django.conf import settings
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import dateparser
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from .models import (
    Resource,
    Tag,
    News,
)


def _get_links_to_news_from_yandex(amount_news):
    """  """
    yandex_home_page = requests.get(settings.YANDEX_NEWS_URL).text
    soup_yandex = BeautifulSoup(yandex_home_page, "html.parser")
    links_yandex_news = list(map(lambda a: a['href'], soup_yandex.find_all("a", class_="link link_theme_normal news-list__item-active i-bem")[:amount_news]))
    return links_yandex_news

def _get_links_to_news_from_ozon(amount_news):
    """  """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    driver.implicitly_wait(60)
    driver.get(settings.OZON_NEWS_URL)
    ##
    button = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div[2]/div/button')
    button.location_once_scrolled_into_view
    ActionChains(driver).click(button).perform()
    ##
    # driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div[2]/div/button').click()
    driver.implicitly_wait(80)
    href_list = driver.find_elements(By.CLASS_NAME, "news-card__link")
    while len(href_list) < amount_news:
        driver.implicitly_wait(80)
        time.sleep(1)
        # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[1]/div/div[2]/div/button'))).click()
        button = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div[2]/div/button')
        button.location_once_scrolled_into_view
        time.sleep(3)
        ActionChains(driver).click(button).perform()
        # driver.execute_script("arguments[0].scrollIntoView(true);", button)
        # button.click()
        href_list = driver.find_elements(By.CLASS_NAME, "news-card__link")
        dates = driver.find_elements(By.CLASS_NAME, "news-card__date")
    links_list = list(map(lambda x: x.get_attribute('href'), href_list[:amount_news]))
    dates_list = list(map(lambda x: x.text, dates[:amount_news]))
    driver.quit()
    return links_list, dates_list

def _parsing_news_yandex(links):
    """  """
    for link in links:
        news = requests.get('https://market.yandex.ru' + link).text
        soup = BeautifulSoup(news, "html.parser")

        title = soup.find("div", class_="news-info__title").get_text()
        date = soup.find("time", class_="news-info__published-date")['datetime']
        text = soup.find("div", class_="news-info__post-body html-content page-content").get_text()

        tag_objects_list = []
        for tag in soup.find_all("a", class_="link link_theme_light-gray news-info__tag i-bem"):
            tag_object, created = Tag.objects.get_or_create(name=tag.get_text()[1:])
            tag_objects_list.append(tag_object)

        resource, created = Resource.objects.get_or_create(name='yandex')
        news_object = News.objects.create(
            title=title,
            text=text,
            resource=resource,
            date=date[:date.find('T')]
        )
        news_object.tags.add(*tag_objects_list)
        news_object.save()

def _parsing_news_ozon(links, dates):
    """  """
    count = 0
    for link in links:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        driver.get(link)
        title = driver.find_element(By.TAG_NAME, "h1").text
        try:
            tags = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div/div/section[1]/div/div[2]/div[2]').text[1:]
        except:
            list_tags = ['Отсутствует']
        else:
            list_tags = tags.split(', #')
        tag_objects_list = []
        for tag in list_tags:
            tag_object, created = Tag.objects.get_or_create(name=tag)
            tag_objects_list.append(tag_object)
        text = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div/section[2]').text
        resource, created = Resource.objects.get_or_create(name='ozon')
        date = dateparser.parse(dates[count]).date()
        news_object = News.objects.create(
            title=title,
            text=text,
            resource=resource,
            date=date
        )
        news_object.tags.add(*tag_objects_list)
        news_object.save()
        count += 1
        driver.quit()

if __name__ == '__main__':
    pass