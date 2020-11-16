class scp():
    def getTitle(number):
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
        
        if (series == 1):
            url = "http://www.scpwiki.com/scp-series"
        else:
            url = "http://www.scpwiki.com/scp-series-{}".format(series)

        print (url)