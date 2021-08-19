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

id_path = os.path.join(git_root, id)
os.makedirs(id_path)

txt_pic = driver.find_elements_by_css_selector('.ntk-lead .ntk-link .ntk-img-path')[0]
#save_img(elements[0], id + '-right')
# elements[0].screenshot(id + '-right.png')

width=txt_pic.size['width']
height=txt_pic.size['height']

pic = driver.find_elements_by_css_selector('.ntk-lead .ntk-link')[0]
#save_img(elements[0], id + '-left')
pic.screenshot('tmp.png')

long_width=pic.size['width']
left=int((int(long_width) - int(width))/2)

im = Image.open('tmp.png')

im = im.crop((left, 0, left + int(width), int(height)))
im.save(os.path.join(id_path, id + '.png'))

header_element = driver.find_elements_by_css_selector('div.ntk-lead .ntk-link a.rapidnofollow h2')[0]
header_link = header_element.find_element_by_xpath('..')
href = header_link.get_attribute('href')
if href[0:1] == '/':
  href = 'https://www.yahoo.com' + href

header = header_element.text
print(header)

if len([t for t in titles if t == header]) > 0:
  print('found header', header)
  driver.quit()
  exit()


content = driver.find_elements_by_css_selector('div.ntk-lead .ntk-link a.rapidnofollow p')[0].text
print(content)
footer = driver.find_elements_by_css_selector('div.ntk-lead .ntk-link a.rapidnofollow p')[1].text

with open(os.path.join(id_path, 'README.md'), 'w') as f:
  f.write('\n!['+ header + '](./'+id+'.png)\n')
  f.write('## ' + header + '\n')
  f.write('\n' + content + '\n')
  f.write('\n![pic](../square_bg.png)\n')
  f.write('\n[' + footer + ']('+href+')\n')

with open(os.path.join(git_root, 'README.md')) as f:
  markdown_content = f.read()


with open(os.path.join(git_root, 'README.md'), 'w') as f:
  f.write('# ['+header+'](./'+id+')\n')
  f.write(markdown_content)

with open('stamp.txt', 'w') as f:
  f.write(id)

with open('titles.txt', 'w') as f:
  f.write(header + '\n')
  for t in titles:
    f.write(t + '\n')

driver.quit()

