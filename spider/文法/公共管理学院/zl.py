# 用来爬图片
import requests
from bs4 import BeautifulSoup
import xlsxwriter
from urllib.parse import urljoin
import re
import csv


class UrlManager:
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url):
        if url is None or len(url) == 0:
            return
        if url in self.new_urls or url in self.old_urls:
            return
        self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def get_url(self):
        if self.has_new_url():
            url = self.new_urls.pop()
            self.old_urls.add(url)
            return url
        else:
            return None

    def has_new_url(self):
        return len(self.new_urls) > 0


base = 'https://wfxy.buct.edu.cn/ggglx/list.htm'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
root_url = "https://wfxy.buct.edu.cn/ggglx/list.htm"
urls = UrlManager()
excelfile = xlsxwriter.Workbook("文法/公共管理学院/1.xlsx")
excel = excelfile.add_worksheet('1')
excel.set_column('A:A', 7)
excel.set_column(1, 2, 50)
# 标题行
headings = ['照片', '名字', '介绍']

# 设置excel风格
excel.set_tab_color('red')
excel.write_row('A1', headings)

path = "文法/公共管理学院/001.csv"


def first():
    num = 0
    r = requests.get(url=root_url, headers=headers)
    if r.status_code != 200:
        print("error:%s %s" % (root_url, r.status_code))
    #print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    # list = soup.find('div' ,class_ = 'box').find_all('a')
    lists = soup.find("ul", 'news_list list2').find_all("a")  
    for l in lists:
        print(l)
        h = l['href']
        num = num + 1
        #print(h)
        # print(type(h))
        print(urljoin(base, h))
        urls.add_new_url(urljoin(base, h))
        print(num)
    print(num)


def craw(url, index):
    print("ready")
    print(url)
    if (url != "https://wfxy.buct.edu.cn/ggglx/list.htm"):
        
        
            rd = requests.get(url=url, headers=headers)
            rd.encoding = 'utf-8'
            soup = BeautifulSoup(rd.text, "html.parser")
            try:
                name = soup.find("div", class_='article').find("h1").get_text()
                print(name)
            except:
                name = "error"
            #print(name)
            
            ps = soup.find("div", class_='entry')
            introduce = ps.find_all('p')
            content_ = ''
            for i in introduce:
                content_ += i.text
                content_ += '\n'
            print("wenbenshuchu")
            print(content_)
            excel.write(index, 1, name)
            excel.write(index, 2, content_)
            #img = ps.find_all('img')

            
            datarow = ['文法/公共管理学院/pic'+name+'.jpg',name, content_]
            with open(path, "a+" ) as f:
              csv_write = csv.writer(f)
              csv_write.writerow(datarow) 

            img = soup.find("div", class_='wp_articlecontent')
            if not (img is None):
                re_url_ = img.find("img")
                #print(re_url_)
                try:
                    re_url = re_url_["src"]
                except:
                    re_url = None
                if re_url is not None:
                    #print(re_url)
                    print("image")
                    #print(re_url)
                    if  (re_url != "<img src=""/>"):
                    #if not(re_url is None):
                    #if not(re.match('.*png$', re_url) is None):
                        image_url = urljoin(url, re_url)
                        print(image_url)
                        try:
                            response = requests.get(image_url, headers = headers)     
                            image = response.content
                        except:
                            image = None
                        if not (image is None ):
                                    
                                with open('文法/公共管理学院/pic/{}.jpg'.format(name), 'wb') as f:
                                    f.write(image)
                                excel.write(index, 0, '文法/公共管理学院/pic' + name + '.jpg')
                                    
                        else:
                            excel.write(index, 0, 'none')




def crawall():
    index = 1
    while urls.has_new_url():
        url = urls.get_url()

        craw(url, index)
        index += 1
    excelfile.close()


if __name__ == '__main__':
    first()
    crawall()
    
