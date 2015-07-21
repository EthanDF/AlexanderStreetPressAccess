#__author__ = 'fenichele'
from pymarc import *
import csv

marcFile = 'c://users/fenichele//desktop//test.mrc'

def testURL(url):
    import requests

    result = 0
    testphrase = 'You do not have access to this page'

    r = requests.get(url)
    rtext = r.text

    if testphrase in rtext:
        result = 1

    return result


def logResults(recordID, title, url, urlresult):
    import time
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    data = [[now, str(recordID), str(title), str(url), str(urlresult)]]

    resultsFile = 'c:\\users\\fenichele\\desktop\\asp.csv'

    with open(resultsFile, 'a', newline='') as out:
        a = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL)
        try:
            a.writerows(data)
        except UnicodeEncodeError:
            data = [[now, str(recordID), 'Title cannot be printed', str(url), str(urlresult)]]
            a.writerows(data)

def readMarc():

    with open(marcFile,'rb') as m:
        reader = MARCReader(m)

        for record in reader:
            # return record
            if record['856'] is None:
                url = None
            else:
                url = record['856']['u']
            recordID = record['001'].value()
            title = record['245']['a']
            # print (url)
            if url is None:
                urlresult = 1
            else:
                urlresult = testURL(url)


            logResults(recordID, title, url, urlresult)


readMarc()






