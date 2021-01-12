import requests
from bs4 import BeautifulSoup as soup
url = 'https://www.philips.co.in/'
link = requests.get(url).text
page = soup(link, 'html.parser')

category = set()
for i in page.find_all('span', class_ = 'p-body-copy-01 p-heading-light p-n02v3__m2text'):
    category.add(i.string.strip())
category = list(category)
print(category,'\n')


nav_bar = page.find('ul', class_ = 'p-n02v3__m2 p-n02v3__micon')
data ={}
a = 'string'
li = nav_bar.find('div',class_ ='p-heading-02 p-heading-light')
for li in nav_bar.findAll('div',class_ ='p-heading-02 p-heading-light'):
    li = li.string
    if li in category:
        a = li
        data[a] = []
    else:
        data[a] += [li]
print(data,'\n')

product_sub_category = []
for li in nav_bar.findAll('li'):
    li = li.findAll('span')[-1].string
    if li not in product_sub_category:
        product_sub_category.append(li)
print(product_sub_category,'\n')

sub_category = {}
# ul =html.find_all('ul', class_ = 'p-n02v3__m4 p-n02v3__m--col24')
for i in page.find_all('ul', class_ = 'p-n02v3__m4 p-n02v3__m--col24'):
    for li in i.find_all('li'):
        sub_category[li.find('span').string.strip()]={}
        a = li.find('a').get('href')
        try:
            new_link = requests.get(a).text
            sub_category_page = soup(new_link,'html.parser')            
            for x in sub_category_page.find_all('div', class_='p-pc05v2__card-info-section--main'):
                sku_url = x.find('a').get('href')
                sku_name = x.find('span',class_='p-heading-light').string.strip()
                product_code = x.find('p').string.strip()
                sub_category[li.find('span').string.strip()][sku_name]={}
                sub_category[li.find('span').string.strip()][sku_name]['Product code'] = product_code
                technical_link = requests.get(sku_url).text
                technical_page = soup(technical_link,'html.parser')
                header = []
                value = []
                for col1 in technical_page.find_all('dt'):
                    header.append(col1.string.strip())

                for col2 in technical_page.findAll('dd'):
                    if col2.find('span'):
                        value.append(col2.find('span').string.strip())
                    else:
                        value.append('')
                sub_category[li.find('span').string.strip()][sku_name]['Technical Specification'] = {}
                for i in range(len(header)):
                    sub_category[li.find('span').string.strip()][sku_name]['Technical Specification'][header[i]] = value[i]
        except:
            pass
print(sub_category)
