import time
from selenium import webdriver
from tqdm import tqdm
import random
import selenium
import os
import pandas as pd

browser = webdriver.Chrome()            # 创建浏览器对象
browser.get('http://news.sina.com.cn/hotnews/')
time.sleep(1)
browser.find_element_by_xpath('//*[@id="Tab12"]').click()
article_list = browser.find_elements_by_xpath('//*[@id="Con12"]/table/tbody/tr')

titles = []
contents = []
content_href = []
comment_href = []
num_comments = []
comments = []

print("获取热点文章链接")

for i in tqdm(range(1,11)):
    item = article_list[i].find_elements_by_tag_name('a')
    content_href.append(item[0].get_attribute('href'))
    titles.append(item[0].get_attribute('textContent'))
    comment_href.append(item[1].get_attribute('href'))
    num_comments.append(item[1].get_attribute('textContent'))

def get_content(url):
    # selenium 模拟
    browser.get(url)
    if 'ent' in url:
        try:
            content_list = browser.find_elements_by_xpath('//*[@id="artibody"]/p')
        except selenium.common.exceptions.NoSuchElementException:
            content_list = []
        
    if 'finance' in url:
        try:
            content_list = browser.find_elements_by_xpath('//*[@id="artibody"]/p')
        except selenium.common.exceptions.NoSuchElementException:
            content_list = []
    if 'news' in url:
        try:
            content_list = browser.find_elements_by_xpath('//*[@id="article"]/p')
        except selenium.common.exceptions.NoSuchElementException:
            content_list = []
    news_content = ''.join([c.text for c in content_list if c.text is not None])
    return news_content
    
def get_comment(url):
    # selenium 模拟
    browser.get(url)
    bottom = None
    cnt = 0
    while bottom is None and cnt < 200:
        print(cnt, end='\r')
        cnt += 1
        try:
            bottom = browser.find_element_by_xpath("//*[text()='更多精彩评论>>']")
        except selenium.common.exceptions.NoSuchElementException:
            bottom = None
        time.sleep(1)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 等待刷新完毕
    time.sleep(3)
    try:
        comment_list = browser.find_elements_by_class_name('txt')
    except selenium.common.exceptions.NoSzuchElementException:
        comment_list = []
    comment_list = [c.text for c in comment_list if c.text is not None]
    return comment_list

print('获取正文')
for url in tqdm(content_href):
    contents.append(get_content(url))
    time.sleep(random.randint(1,3))

print('获取评论')
for url in tqdm(comment_href):
    comments.append(get_comment(url))
    time.sleep(random.randint(1,3))

print('保存数据')
base_dir = str(time.strftime("%Y-%m-%d", time.localtime()))
if not os.path.isdir(base_dir):
    os.mkdir(base_dir)

data = {'title': titles,
        'href': content_href,
        'content': contents,
        'num_comments': num_comments}
df = pd.DataFrame(data)
df.to_csv(base_dir+'news.csv')

for i in range(len(comments)):
    df = pd.DataFrame(comments[i])
    df.to_csv(base_dir+f'/{i}.csv')