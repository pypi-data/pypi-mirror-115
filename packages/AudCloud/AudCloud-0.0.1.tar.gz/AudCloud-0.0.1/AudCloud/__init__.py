import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import speech_recognition as sr
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

fname = input("Enter File name with .wav extension \n")


def ac(name):
    r = sr.Recognizer()
    r.energy_threshold = 300
    
    with sr.AudioFile(name) as source:
        try:
            audio_file = r.record(source)
            result = r.recognize_google(audio_data=audio_file)
            print(result)
        
        except:
             print('Sorry.. run again...')


    wc = WordCloud(background_color = 'white', width = 1920, height = 1080)
    wc.generate_from_text(result)
    wc.to_file('wc.png')
    plt.imshow(wc)


ac(fname)