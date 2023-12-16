import pyttsx3
import time
import re

def text_to_speech(text, speed=150, stop_after_fullstop=3, words_pause=5):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)

    # mapping gilak punctuation marks gilak or karone 
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

        # sentence bur ata ata words le split kore
        words = sentence.split()

        # atui 5 words group to speak kore at a time
        for i in range(0, len(words), words_pause):
            group = ' '.join(words[i:i+words_pause])
            engine.say(group)
            engine.runAndWait()

            time.sleep(1)  # 1 second or delay disu nijor mote set kori lole a hol

        
        if sentence.endswith('full stop '):
            time.sleep(stop_after_fullstop)
        else:
            time.sleep(1)  

if __name__ == "__main__":
    # Example tu yet a bohale a hol
    input_text = "Fun is a subjective and enjoyable experience that brings pleasure, amusement, or a sense of entertainment. It often involves activities, experiences, or interactions that people find enjoyable, lighthearted, and engaging. What is considered fun can vary widely from person to person, as individual preferences, interests, and cultural backgrounds play a significant role in shaping one's perception of enjoyment. Fun can be found in various forms, such as playing games, socializing with friends, engaging in hobbies, watching movies, or experiencing new and exciting things. Ultimately, the concept of fun is personal and can encompass a wide range of positive and enjoyable experiences."

    # COnfig 
    dictation_speed = 90  # words per minute
    stop_after_fullstop = 1  # Stop in seconds after a full stop
    words_pause = 5  # Pause after every 5 words

    text_to_speech(input_text, dictation_speed, stop_after_fullstop, words_pause)


# Your code is reday to use brooooooo! 
