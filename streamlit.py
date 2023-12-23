'''
Name: dictatemyhomework
Author: AnubhavSC and moiSentineL
Repo: https://github.com/moiSentineL/dictatemyhomework
Version: 0.3
'''

import pyttsx3
import streamlit as st
import time
import re

def text_to_speech(text, speed, stop_after_fullstop, word_group, pause_after):
    engine = pyttsx3.init()
    engine.endLoop()
    engine.startLoop(False)
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
        # engine.startLoop(False)
        for i in range(0, len(words), word_group):
            group = ' '.join(words[i:i+word_group])
            engine.say(group)
            engine.iterate()

            time.sleep(pause_after)  # Delay after speaking

        # Delay after full stop
        if sentence.endswith('fullstop '):
            time.sleep(stop_after_fullstop)
        else:
            time.sleep(pause_after) 


if __name__ == "__main__":
    st.title('Dicto')
    st.header('For the clever students', divider=True)
    input_text = st.text_area(
    "Text to speak:",
    "",)
    
    with st.sidebar:
        st.subheader('Configuration', divider=True)
        dictation_speed = st.slider('Set Speech Rate (in Words Per Minute)', 75, 360, 90)
        stop_after_fullstop = st.slider('Pause after fullstops (in seconds)', 0, 10, 1)
        word_group = st.slider('No. of words in one group', 1, 10, 4)
        pause_after = st.slider('Pause after each group (in seconds)', 0, 20, 8)


    # Old Config 
    # dictation_speed = 90  # words per minute
    # stop_after_fullstop = 1  # Stop in seconds after a full stop
    # word_group = 5  # Word Group
    # pause_after = 7 # Pausing after speaking each word group

    if st.button('Speak!'):
        # try:
        #     text_to_speech(input_text, dictation_speed, stop_after_fullstop, word_group, pause_after)
        # except Exception as e:
        #     print(e)
        text_to_speech(input_text, dictation_speed, stop_after_fullstop, word_group, pause_after)
   
    else:
        pass
