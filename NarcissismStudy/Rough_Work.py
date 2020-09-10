from watson_developer_cloud import ToneAnalyzerV3
import time

specs1_counter = 1
spec2_counter = 1
specs3_counter = 1
spec4_counter = 1

def specs1(): #vu.nl
    apikey = 'Sst3Vq2D221Alx-YbgLNtwOyu5fywKtaL2rl8NSl9-m3'
    urlref = 'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/2ba5653f-b626-495a-9efc-c9e3f6428c59'#'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/618c6917-36fa-4dd7-a10b-8df2ed184446'
    version = '2/25/2020'#'2020-02-20'#'2020-02-21'
    return apikey,urlref,version
def specs2():   #yahoo
    apikey = 'wGySQLw3nxEOhEirYSvAZScum9v_1_VoA8lKZYMi6ip-'
    urlref = 'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/618c6917-36fa-4dd7-a10b-8df2ed184446'
    version = '2020-02-20'
    return apikey,urlref,version

def specs3(): #pucit
    apikey = 'mIP78HW3wcpGenbSz5bI1MSaNirbXp1wMh9ShD00K9--'
    urlref = 'https://api.eu-de.tone-analyzer.watson.cloud.ibm.com/instances/18fed176-e3c8-4b9a-9f2d-048b53bcd84a'
    version = '2020-02-21' #FEB 21, 2020 - 12:06:33 AM
    return apikey,urlref,version

def specs4():#hotmail
    apikey = 'oLWVV0QsjJaBzwTTeOxS2sPx804uxTarCFVlKkPvCV05'
    urlref = 'https://api.au-syd.tone-analyzer.watson.cloud.ibm.com/instances/27427a84-0402-4256-a758-ca5fe0fd53c9'
    version = '2020-09-09' #SEP 9, 2020 - 04:49:51 PM
    return apikey,urlref,version

from numpy import random
def initializeAnalyzer():
    # we imported time because ToneAnalyzer versions have YYYY-MM-DD format


    currentVersion = time.strftime("%Y-%m-%d")
    print_string = "Using Tone Analyzer\'s version: " + str(currentVersion)
    print("=" * len(print_string))
    print( print_string)
    print ("=" * len(print_string))
    tone_analyzer3 = ToneAnalyzerV3(
            version=currentVersion,
            iam_apikey=apikey,
            url=urlref
    )


    return tone_analyzer3

if __name__ == '__main__':
    apikey, urlref, version = specs1()
    analyzer1 = initializeAnalyzer(apikey, urlref, version)
    apikey, urlref, version = specs2()
    analyzer2 = initializeAnalyzer(apikey, urlref, version)
    apikey, urlref, version = specs3()
    analyzer3 = initializeAnalyzer(apikey, urlref, version)
    apikey, urlref, version = specs4()
    analyzer4 = initializeAnalyzer(apikey, urlref, version)

    nummer = random.randint(4)
    analyzer = 1
    if nummer == 1:
        analyzer = analyzer1
    else:
        if nummer == 2:
            analyzer = analyzer2
        else:
            if nummer == 3:
                analyzer = analyzer3
            else:
                analyzer = analyzer4



    i = 0
    while(i < 10):
        text = "I am happy"
        tone_analysis = analyzer.tone({'text': text}, content_type='application/json').get_result()
