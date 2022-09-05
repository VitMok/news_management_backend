if __name__ == '__main__':
    from selenium import webdriver
    # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    # driver.implicitly_wait(60)
    # driver.get('https://seller.ozon.ru/news')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    chrome_driver_path = "C:\Python27\Scripts\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path, options=options)