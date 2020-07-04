import sqlite3
conn = sqlite3.connect('project/db.sqlite3')

'''print("Opened database successfully")
res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in res:
     print(name[0])
'''






exit(0)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
#ref: https://www.codetable.net/unicodecharacters?page=89
happy = [128513,128514,128515,128516,128517,128518,128519,128520,128521,128522,128523,128524
    ,128525,128526,128536,128538,128540,128541,128568,128569,128570,128571,128572 ,128573
    ,128584,128585,128586 #cats
    ,128587,128588,128591 #monkeys
    ,10084,10083,10085,10086,10087 #black hearts
    ]
neutral = [128527,128528,128530,128554,128555,128562,128563,128565,128566,128567,128582]
anxiety = [128531,128532,128534]
angry = [128542,128544,128545,128574,128581,128589,128590]
sad = [128546,128547,128548,128549,128553,128557,128560,128575,128576]
fear = [128552,128561]

def checkemoji(text):
    for ch in text:
       ord_value = ord(ch)
       if(happy.__contains__(ord_value)):
            return "Happy",0.8
       else:
            if (neutral.__contains__(ord_value)):
                return "Neutral",0.0
            else:
                if (anxiety.__contains__(ord_value)):
                    return "Anxiety",-0.1
                else:
                    if (angry.__contains__(ord_value)):
                        return "Angry",-0.8
                    else:
                        if (sad.__contains__(ord_value)):
                            return "Sad",-0.4
                        else:
                            if (fear.__contains__(ord_value)):
                                return "Tentative",0.0
    return "no_emoji",0.0

text = '@mahee2000 love this ❤️ more love, less hate'
#text = '🙈❤️.'

vs = analyzer.polarity_scores(text)
score = vs['compound']
if (score >= 0.05):
    tone_name = "Positive"
else:
    if(score > -0.05 and score < 0.05):
        tone_name,score = checkemoji(text)
    else:
        if(score <= -0.05):
            tone_name = "Negative"
print(tone_name + str(score))
