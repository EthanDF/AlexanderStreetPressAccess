#__author__ = 'fenichele'
from pymarc import *
import csv

marcFile = 'faavonallb.mrc'

def testURL(url):
    import requests

    result = 0
    testphraseList = ['You do not have access to this page', 'HTTP Error 500 - Internal Server Error']

    r = requests.get(url)
    rtext = r.text

    for phrase in testphraseList:
        if phrase in rtext:
            result = 1

    return result


def logResults(recordID, title, url, urlresult):
    import time
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    data = [[now, str(recordID), str(title), str(url), str(urlresult)]]

    resultsFile = 'accessChecks.csv'

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
        counter = 0


        for record in reader:
            urlList = []
            counter += 1

            startRecord = 4860
            if counter < startRecord:
               continue
            else:
                print('starting with record '+str(startRecord))
			
            # return record
            if record['856'] is None:
                urls = None
            else:
                urls = record.get_fields('856')
                # print(url)
            recordID = record['001'].value()
            title = record['245']['a']
            # print (url)
            if urls is None:
                url = None
                urlresult = 1
            else:
                for x in urls:
                    if x['u'] is None:
                        url = None
                    elif x['u'].replace('http://ezproxy.fau.edu/login?url=','') not in urlList:
                        urlList.append(x['u'].replace('http://ezproxy.fau.edu/login?url=',''))
                    else:
                        url = None

                for url in urlList:
                    urlresult = testURL(url)
                    logResults(recordID, title, url, urlresult)


            continueTest = 'y'
            # continueTest = str(input('continue? press "n" to stop'))
            if continueTest == 'n':
                print(1/0)


readMarc()






