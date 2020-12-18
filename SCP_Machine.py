import re
from PIL import Image,ImageTk
import requests
from bs4 import BeautifulSoup


class scp:
    @classmethod
    def getTitle(self, number):

        Title = None

        print(number)
        series = scp.getSeries(number)

        if series == 1:
            url = "http://www.scpwiki.com/scp-series"
        else:
            url = "http://www.scpwiki.com/scp-series-{}".format(series)

        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="page-content")

        lists = results.find_all("ul")
        for i in lists:
            if list == None:
                continue
            else:
                searchPattern = "-{0}</a> - ((.*?))</li>".format(number)
                Title = re.search(searchPattern, str(i))
                if Title == None:
                    continue
                else:
                    Title = str(Title.group(1))
                    break

        return Title

    @classmethod
    def getSeries(self, number):

        # number = self.number

        series = 0
        if number < 1000:
            series = 1
        elif number < 2000:
            series = 2
        elif number < 3000:
            series = 3
        elif number < 4000:
            series = 4
        elif number < 5000:
            series = 5
        elif number < 6000:
            series = 6

        return int(series)


    @classmethod
    def getImage(self, pageContent):
        img_Temp = pageContent.find_all('div', class_='scp-image-block block-right')
        img_Temp = re.search('src="((.*?))"', str(img_Temp))
        if (img_Temp != None):  
            print(img_Temp) 
            url = str(img_Temp.group(1))
            print (url)
        else:
            return None

        response = requests.get(url)

        file = open("images/imageDownload.png", "wb")
        file.write(response.content)
        file.close()

        global scpImage
        scpImage = Image.open("images/imageDownload.png")
        if(scpImage.size[1] > scpImage.size[0]):
            width = (160/scpImage.size[1]) * scpImage.size[0]
            height = 160
        else:
            height = (160/scpImage.size[0]) * scpImage.size[1]
            width = 160
        
        scpImage = scpImage.resize((round(width), round(height)))
        final_scpImage = ImageTk.PhotoImage(scpImage)
        return final_scpImage

    @classmethod
    def getObjectClass(self, pageElements):
        for i in pageElements:
            objectClass = re.search("Object Class:</strong> ((.*?))</p>", str(i))
            if objectClass == None:
                continue
            objectClass = str (objectClass.group(1))

            # This is code for extracting the class from elements with different styles (ex. scp-1762, scp-3987)
            if (re.search("<span style=((.*?));",objectClass)== None and re.search("<span style=((.*?))</span>",objectClass)== None):
                objectClass = "\nObject class: {}".format(str(objectClass))
            elif (re.search("<span style=((.*?));",objectClass) != None):
                objectClass = re.search("</span> ((.*?))</p>", str(i))
                objectClass = str(objectClass.group(1))
                objectClass = "\nObject class: {}".format(str(objectClass))
            elif (re.search("<span style=((.*?))</span>",objectClass) != None):
                objectClass = re.search('">((.*?))</span>', str(i))
                objectClass = str(objectClass.group(1))
                objectClass = "\nObject class: {}".format(str(objectClass))
            
            print(objectClass)
            return objectClass

    @classmethod
    def getRating(self, pageContent):
        rating_Temp = pageContent.find('span', class_='number prw54353')
        rating_Temp = re.search('prw54353">((.*?))</span>', str(rating_Temp))

    @classmethod
    def getSize(self):
        size = [scpImage.size[0],scpImage.size[1]]
        return size