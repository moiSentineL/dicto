import os
import pyttsx3
import sys
import time
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re

speed_variable = 99
pause_after_words_variable = 5
delay_after_fullstop_variable = 1

def text_to_speech(text, speed=speed_variable, stop_after_fullstop=delay_after_fullstop_variable, words_pause=pause_after_words_variable):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    
    punctuation_mapping = {
        '.': 'full stop',
        ',': 'comma',
        '?': 'question mark',
        '!': 'exclamation mark',
        ';': 'semicolon',
        ':': 'colon',
    }
    sentences = re.split(r'(?<=[.!?;:])\s+', text)

    for sentence in sentences:
        for punctuation, spoken_word in punctuation_mapping.items():
            sentence = sentence.replace(punctuation, f'{spoken_word} ')

        words = sentence.split()

        for i in range(0, len(words), words_pause):
            group = ' '.join(words[i:i+words_pause])
            engine.say(group)
            engine.runAndWait()
            time.sleep(1)

        if sentence.endswith('full stop '):
            time.sleep(stop_after_fullstop)
        else:
            time.sleep(1)

main = tk.Tk()
main.resizable(False, False)
main.configure(background='black')

window_height = 95
window_width = 425

screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2.5) - (window_height/2))

l1 = tk.Label(main, text="Speak: ", font=("Calibri", 12), bg="black", fg="white")
l1.grid(row=2, column=0, sticky=tk.W, pady=15, padx=5)

speakentry = tk.Entry(main, width=37)
speakentry.grid(row=2, column=1, pady=2)

l2 = tk.Label(main, text="Voice: ", font=("Calibri", 12), bg="black", fg="white")
l2.grid(row=3, column=0, sticky=tk.W, pady=0, padx=5)

combo = ttk.Combobox(main, values='Male Female', width=10)
combo.set('Select')
combo.grid(row=3, column=1, pady=0)
combo.place(x=71, y=60)

def voice(key):
    input_text = speakentry.get()
    text_to_speech(input_text)

def voice_b():
    if combo.get() == 'Male':
        voiceid = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'

        engine = pyttsx3.init()
        engine.setProperty('rate', speed_variable)
        engine.setProperty('voice', voiceid)
        input_text = speakentry.get()
        text_to_speech(input_text)

    elif combo.get() == 'Female':
        voiceid = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

        engine = pyttsx3.init()
        engine.setProperty('rate', speed_variable)
        engine.setProperty('voice', voiceid)
        input_text = speakentry.get()
        text_to_speech(input_text)

    else:
        tk.messagebox.showerror('Error 069', 'No voice id selected. Kindly select it')

def exit(key):
    sys.exit()

def save():
    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%y; %I:%M:%S %p')
    times = sttime + '.mp3'

    if combo.get() == 'Male':
        voiceid = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'

        engine = pyttsx3.init()
        engine.setProperty('rate', speed_variable)
        engine.setProperty('voice', voiceid)
        engine.save_to_file(speakentry.get(), "speakerbot_output.mp3")
        engine.runAndWait()

    elif combo.get() == 'Female':
        voiceid = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

        engine = pyttsx3.init()
        engine.setProperty('rate', speed_variable)
        engine.setProperty('voice', voiceid)
        engine.save_to_file(speakentry.get(), "speakerbot_output.mp3")
        engine.runAndWait()

    elif combo.get() == 'Select':
        tk.messagebox.showerror('Error 069', 'No voice id selected. Kindly select it')
    else:
        tk.messagebox.showerror('Error 420', 'Error selecting voice ID. Please recheck')

def clear():
    speakentry.delete(0, 'end')

main.bind('<Return>', voice)
main.bind('<Escape>', exit)

speakentry_button = tk.Button(main, text="ok", command=voice_b)
speakentry_button.grid(row=2, column=2, padx=15)

save_button = tk.Button(main, text="save", command=save)
save_button.grid(row=3, column=2)

clear_button = tk.Button(main, text="clear", command=clear)
clear_button.grid(row=3, column=1,)
clear_button.place(x=327, y=59,)

main.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
main.title('speakerbot 2.1')
main.mainloop()
