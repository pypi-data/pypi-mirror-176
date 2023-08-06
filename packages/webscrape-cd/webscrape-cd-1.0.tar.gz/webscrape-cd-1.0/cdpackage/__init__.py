from googlesearch import search
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import csv
#import speech_recognition
#import phonenumbers
#rec = speech_recognition.Recognizer()
#from gtts import gTTS

'''try:
    with speech_recognition.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic, duration=1)
                print("Listening")
                audio=rec.listen(mic)
                query=rec.recognize_google(audio)
                print(query)
except:
    pass'''
def contact_finder(query, startno, numqu):
    url = []
    for j in search(query, num=10,pause=2, start = startno-1, stop = startno + numqu-1):
        url.append(j)
    title = []
    emails = []
    #numbers = []
    for i in url:
        try:
            text = requests.get(i).text
            soup = BeautifulSoup(text,'lxml')
            title.append(soup.title.string)
            text = re.compile(r'<[^>]+>').sub('', text)
            email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
            #number = phonenumbers.PhoneNumberMatcher(text, 'IN')
            #num=[]
            #for i in number:
            #    num.append(number)
            emails.append(email)
            #numbers.append(num)
        except:
            title.append('Error Occured')
            emails.append('Error Occured')

    #arr = np.array([title, url])
    #print(np.matrix(arr))
    #table = PrettyTable(['Title', 'URL', 'Emails'])
    #for i in range(len(url)):
    #    table.add_row([title[i], url[i], emails[i]])
    #print(table)
    arr_final = []
    for i in range(len(url)):
        arr_final.append([title[i], url[i], emails[i]])
    with open('school.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Title','URL','Emails'])
        csvwriter.writerows(arr_final)