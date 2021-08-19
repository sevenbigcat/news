from selenium import webdriver
import datetime
from PIL import Image
import os

print('grab news from yahoo')

with open('stamp.txt', 'w') as f:
  f.write('')

if not os.path.exists('titles.txt'):
  with open('titles.txt', 'w') as f:
    f.write('')

with open('titles.txt') as f:
  titles = [t for t in f.read().split('\n') if t != '']

print('there are', len(titles), 'titles')

git_root = '.'

options=webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--start-maximized')
options.add_argument('user-data-dir=./user-data')
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
driver.get('https://www.yahoo.com')

now = datetime.datetime.now()
id = now.strftime('%Y%m%d%H%M%S')
print(id)


driver.quit()
