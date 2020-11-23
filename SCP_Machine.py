import re
import requests
from bs4 import BeautifulSoup

class scp():

    number = 0

    @classmethod
    def getTitle(self,number):
        
        Title = None

        print(number)
        series = scp.getSeries(number)
        toc = scp.getToc(number)

        if (series == 1):
            url = "http://www.scpwiki.com/scp-series"
        else:
            url = "http://www.scpwiki.com/scp-series-{}".format(series)

        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='page-content')

        lists = results.find_all('ul')
        for i in lists:
            if list == None:
                continue
            else:
                searchPattern = '-{0}</a> - ((.*?))</li>'.format(number)
                Title = re.search(searchPattern,str(i))
                if Title == None:
                    continue
                else:
                    Title = str(Title.group(1))
                    break

        return Title

    @classmethod
    def getSeries(self,number):

        #number = self.number

        series = 0
        if (number < 1000):
            series = 1
        elif(number < 2000):
            series = 2
        elif(number < 3000):
            series = 3
        elif(number < 4000):
            series = 4
        elif(number < 5000):
            series = 5
        elif(number < 6000):
            series = 6
        
        return int(series)

    @classmethod
    def getToc(self,number):
        
        #number = self.number
        toc = 0
        series = scp.getSeries(number)

        if (number - ((series-1)*1000) < 100):
            toc = 2
        elif(number - ((series-1)*1000) < 200):
            toc = 3
        elif(number - ((series-1)*1000) < 300):
            toc = 4
        elif(number - ((series-1)*1000) < 400):
            toc = 5
        elif(number - ((series-1)*1000) < 500):
            toc = 6
        elif(number - ((series-1)*1000) < 600):
            toc = 7
        elif(number - ((series-1)*1000) < 700):
            toc = 8
        elif(number - ((series-1)*1000) < 800):
            toc = 9
        elif(number - ((series-1)*1000) < 900):
            toc = 10
        elif(number - ((series-1)*1000) < 1000):
            toc = 11
        
        return toc

    def setNumber(self,newNumber):
       self.number = newNumber
