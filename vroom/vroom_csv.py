
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time

driver = webdriver.Chrome(r'C:\Users\hk486\chromedriver.exe')
driver.maximize_window()
driver.get("https://www.vroom.com/cars/?filters=eyJzZWFyY2giOiIiLCJwcmljZSI6eyJtaW4iOjIyMTQ1LCJtYXgiOjI5NTI3fX0=")

csv_file = open('vroom.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

page = 1

while True:
    try:
        print('='*50)
        print(f'Scarping page {page}')

        wait_product = WebDriverWait(driver, 7.5)
        products = wait_product.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-md-3"]')))

        for product in products:
            product_dict = {}

            driver.execute_script("arguments[0].scrollIntoView();", product)

            year = product.find_element_by_xpath('./div[1]/a[1]/div[2]/p[1]').text.split()[0]
            print(f'year: {year}')

            brand = product.find_element_by_xpath('./div[1]/a[1]/div[2]/p[1]').text.split()[1]
            if brand in ['Alfa', 'Land']:
                brand = ' '.join(product.find_element_by_xpath('./div[1]/a[1]/div[2]/p[1]').text.split()[1:3])
                print(f'brand: {brand}')
                model = ' '.join(product.find_element_by_xpath('./div[1]/a[1]/div[2]/p[1]').text.split()[3:])
                print(f'model: {model}')
            else:
                print(f'brand: {brand}')
                model = ' '.join(product.find_element_by_xpath('./div[1]/a[1]/div[2]/p[1]').text.split()[2:])
                print(f'model: {model}')

            trim = product.find_element_by_xpath('./div[1]/a[1]/div[2]/div[1]/p[1]').text
            print(f'trim: {trim}')

            miles = int(product.find_element_by_xpath('./div[1]/a[1]/div[2]/div[1]/p[3]').text.split()[0].replace(',', ''))
            print(f'miles: {miles}')

            price = product.find_element_by_xpath('./div[1]/a[1]/div[2]/p[2]').text
            print(f'price: {price}')
            print('='*50)

            product_dict['year'] = year
            product_dict['brand'] = brand
            product_dict['model'] = model
            product_dict['trim'] = trim
            product_dict['miles'] = miles
            product_dict['price'] = price

            writer.writerow(product_dict.values())

        wait_next_button = WebDriverWait(driver, 7.5)
        next_button = wait_next_button.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Go to next page"]')))
        next_button.click()
        time.sleep(1)

        print('='*50)
        print('Next button clicked')

        page += 1

    except Exception as e:
        print('='*10)
        print(e)
        csv_file.close()
        driver.close()
        break
