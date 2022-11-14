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


base = 'https://cmp.buct.edu.cn/688/list.htm'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
root_url = "https://cmp.buct.edu.cn/688/list.htm"
urls = UrlManager()
excelfile = xlsxwriter.Workbook("/Users/apple/Desktop/buct/1.xlsx")
excel = excelfile.add_worksheet('1')
excel.set_column('A:A', 7)
excel.set_column(1, 2, 50)
# 标题行
headings = ['照片', '名字', '介绍']

# 设置excel风格
excel.set_tab_color('red')
excel.write_row('A1', headings)

path = "/Users/apple/Desktop/buct/001.csv"


def first():
    num = 0
    r = requests.get(url=root_url, headers=headers)
    if r.status_code != 200:
        print("error:%s %s" % (root_url, r.status_code))
    #print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    # list = soup.find('div' ,class_ = 'box').find_all('a')
    lists = soup.find("div", 'subPastLeaderBox').find_all("a")
    for l in lists:
        #print(l)
        
        h = l['href']
        num = num + 1
        #print(h)
        # print(type(h))
        print(urljoin(base, h))
        urls.add_new_url(urljoin(base, h))
        
    print(num)


def craw(url, index):
    print("ready")
    print(url)
    if (url != "https://cmp.buct.edu.cn/wlxb/list.htm")&(url != "https://cmp.buct.edu.cn/688/list.htm")&(url != "https://cmp.buct.edu.cn/sxxb/list.htm")&(url != "https://cmp.buct.edu.cn/yjg/list.htm"):
        
        
            rd = requests.get(url=url, headers=headers)
            rd.encoding = 'utf-8'
            soup = BeautifulSoup(rd.text, "html.parser")
            try:
                name = soup.find("div", class_='subArticle_left').find("h2").get_text()
                print(name)
            except:
                name = "error"
            #print(name)
            content_ = ''
            ps = soup.find("div", class_='subLeaderDetail_info')
            
            if  not (  ps is None):
                introduce = ps.find_all('p')
                for i in introduce:
                    content_ += i.text
                    content_ += '\n'
                
                
            excel.write(index, 1, name)
            excel.write(index, 2, content_)
                #img = ps.find_all('img')

            
            datarow = ['/Users/apple/Desktop/buct/pic/'+name+'.jpg',name, content_]
            with open(path, "a+" ) as f:
              csv_write = csv.writer(f)
              csv_write.writerow(datarow) 
              
            img = soup.find("div", class_='subLeaderDetail_img')
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
                                    
                                with open('/Users/apple/Desktop/buct/pic/{}.jpg'.format(name), 'wb') as f:
                                    f.write(image)
                                excel.write(index, 0, '/Users/apple/Desktop/buct/pic/' + name + '.jpg')
                                    
                        else:
                            excel.write(index, 0, 'none')

            

        #print(index)


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
    
