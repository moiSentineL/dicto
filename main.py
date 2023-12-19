'''
Name: dictatemyhomework
Author: AnubhavSC and moiSentineL
Repo: https://github.com/moiSentineL/dictatemyhomework
Version: 0.2
'''

import pyttsx3
import time
import re

def text_to_speech(text, speed, stop_after_fullstop, word_group, pause_after):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)

    punctuation_mapping = {
        '.': 'fullstop',
        ',': 'comma',
        '?': 'questionmark',
        '!': 'exclamationmark',
        ';': 'semicolon',
        ':': 'colon',
    }
    sentences = re.split(r'(?<=[.!?;:])\s+', text)

    for sentence in sentences:
        for punctuation, spoken_word in punctuation_mapping.items():
            sentence = sentence.replace(punctuation, f' {spoken_word} ')
        
        # Splits sentences into words
        words = sentence.split()

        punctuations = ['fullstop', 'comma', 'questionmark', 'exclamationmark', 'semicolon', 'colon']
        indices = [i for i in range(len(words)) if words[i] in punctuations]

        # print (indices)

        # Speaks word group
        for i in range(0, len(words), word_group):
            group = ' '.join(words[i:i+word_group])
            engine.say(group)
            engine.runAndWait()

            time.sleep(pause_after)  # Delay after speaking
        
        # Delay after full stop
        if sentence.endswith('fullstop '):
            time.sleep(stop_after_fullstop)
        else:
            time.sleep(pause_after)  

if __name__ == "__main__":

    input_text = input("Enter Text for TTS: ")

    # Config 
    dictation_speed = 90  # words per minute
    stop_after_fullstop = 1  # Stop in seconds after a full stop
    word_group = 5  # Word Group
    pause_after = 7 # Pausing after speaking each word group

    try:
        text_to_speech(input_text, dictation_speed, stop_after_fullstop, word_group, pause_after)
    except Exception as e:
        print(e)        
