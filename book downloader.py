import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup


downloadList = {}
fileSizes = []
booksCount = 0
maxPage = 10
baseUrl = 'http://www.amarbooks.com/cat.php?cd=155&pg='

def Download(url, name, fileSize):
    print('======================================')
    print(name + ' : Downloading...')
    print(fileSize)
    urllib.request.urlretrieve(url, name)


def Crawl(url, pageNo):
    url = url + str(pageNo)
    try:
        source = BeautifulSoup(requests.get(url).content)
        divs = source.find_all('div', {'style': 'margin: 5px 0 0 0; padding: 0 10px 0 0'})
        fileSize = source.find_all('div', {'style': 'font-size: 14px; color: #aaaaaa'})
        for div in divs:
            name = div.string.split('. ')[1]
            url = 'http://www.amarbooks.com/pdfs/Masud%20Rana%20Series/' + name.replace(' ', '%20') + '.pdf'
            downloadList[name] = {'name': name + '.pdf', 'url': url}
        for x in fileSize:
            fileSizes.append(x.string)
        num = 1
        for key in downloadList.keys() and x in range(len(fileSizes)):
            book = downloadList[key]
            Download(book['url'], book['name'], fileSizes[x])
            print(book['name'] + ': Download finished.')
            num += 1
            print('======================================\n\n')
        pageNo += 1
        Crawl(baseUrl, pageNo)
    except Exception as e:
        print(str(e))

Crawl(baseUrl, 3)
