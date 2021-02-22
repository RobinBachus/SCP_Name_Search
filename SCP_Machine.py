import glob
import os
import re
from PIL import Image,ImageTk
import requests
from bs4 import BeautifulSoup


class scp:

    @classmethod
    def getTitle(self, number):

        Title = None

        series = scp.getSeries(number)

        if series == 1:
            url = "http://www.scpwiki.com/scp-series"
        else:
            url = "http://www.scpwiki.com/scp-series-{}".format(series)

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
                    TitleStrong = re.search("<strong>((.*?))</strong>", Title)
                    if (TitleStrong != None):
                        Title = re.search("((.*?)) - <strong>", Title)
                        Title = str(Title.group(1))
                        TitleStrong = str(TitleStrong.group(1))

                        Title = "{} - {}".format(Title, TitleStrong)
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
    def DownloadImages(self, pageContent): # Test scp: 4015
        
        # clear previous images
        files = glob.glob('TestFiles/images/imageDownload*.png')
        for f in files:
            os.remove(f)

        # find images from current scp
        img_Temp = pageContent.find_all('div', class_='scp-image-block block-right')
        img_Temp = re.findall('src="((.*?))"', str(img_Temp), re.DOTALL)
        if (len(img_Temp) != 0): 
            # download all available images 
            counter = 0
            for i in img_Temp:
                response = requests.get(i[0])

                counter+=1
                imageLocation = "TestFiles/images/imageDownload{}.png".format(counter)
                file = open(imageLocation, "wb")
                file.write(response.content)
                file.close()
            return len(img_Temp)
        else:
            return 1


    @classmethod
    def getImage(self, index):
        global scpImage

        try:
            scpImage = Image.open("TestFiles/images/imageDownload{}.png".format(index))
        except:
            return None

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
        counter = 0
        for i in pageElements:
            counter += 1
            objectClass = re.search("Object Class:</strong> ((.*?))</p>", str(i))
            if objectClass == None:
                if (counter == len(pageElements)):
                    objectClass = "\nobject class: object class not found"
                    return objectClass
                else:
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
            else:
                objectClass = "\nobject class: object class not found"
            
            print(objectClass)
            return objectClass

    @classmethod
    def getRating(self, pageContent):
        rating_Temp = pageContent.find('span', class_='number prw54353')
        rating_Temp = re.search('prw54353">((.*?))</span>', str(rating_Temp))
        return rating_Temp

    @classmethod
    def getSize(self):
        size = [scpImage.size[0],scpImage.size[1]]
        return size