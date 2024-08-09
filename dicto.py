from gtts import gTTS
import pygame
import io
import time
import re
import os
import sys
import argparse
import base64
import streamlit as st

pygame.init()  # outside class?
pygame.mixer.init()

class dicto:
    def __init__(self):
        self.punctuation_mapping = {
            ".": "full stop",
            ",": "comma",
            "?": "question mark",
            "!": "exclamation mark",
            ";": "semicolon",
            ":": "colon",
            "-": "hyphen",
        }
        with st.sidebar:
            self.lang = "en" # st.selectbox(
            #             "Language",
            #             ("Email", "Home phone", "Mobile phone"),
                    # ) #"en"
            self.tld =  "co.uk" #st.selectbox(
                    #     "How would you like to be contacted?",
                    #     ("Email", "Home phone", "Mobile phone"),
                    # ) # "co.uk"
            self.stop_after_fullstop = st.slider("Pause after fullstop (s)", 0.0, 5.0, 1.5) # 1.5
            self.word_group = st.slider("How many words at once?", 0, 5, 2) #2
            self.base_pause = st.slider("Minimum pause", 0.0, 5.0, 0.5)  # 0.5
            # self.extra_pause_frequency = 2
            # self.extra_pause_duration = 1.2
            self.length_multiplier = st.slider("Length Multiplier", 0.0, 1.0, 0.135)  # 0.135

    # def autoplay_audio(audio_data: str):
        
        # b64 = base64.b64encode(audio_data.getvalue()).decode()
        # md = f"""
        #     <audio style="display:none" controls autoplay="true">
        #     <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        #     </audio>
        #     """
        # st.markdown(
        #     md,
        #     unsafe_allow_html=True,
        # )

    def speak_group(self, group, is_last_group):
        fp = io.BytesIO()
        tts = gTTS(text=group, lang=self.lang, tld=self.tld, slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)

        # dicto.autoplay_audio(fp)

        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        if not is_last_group:
            time.sleep(
                self.base_pause
                + ((sum(len(word) for word in group.split())) * self.length_multiplier)
            )

    def display_paragraph(self, paragraph, current_group):  
        # os.system("cls" if os.name == "nt" else "clear")  # Clear console

        highlighted = []
        current_group_words = current_group.split()

        i = 0
        while i < len(words := paragraph.split()):
            if (
                to_be_h := words[i : i + len(current_group_words)]
            ) == current_group_words:  # i + len(current_group_words) <= len(words) and
                highlighted.append(f":red[{' '.join(to_be_h)}]")
                i += len(current_group_words)
            else:
                highlighted.append(words[i])
                i += 1
        return " ".join(highlighted)

    def dictate(self, text):
        for paragraph in (paragraphs := text.split("\n")):
            i = 0
            while i < len(words := paragraph.split()):
                group = []
                display_group = []

                for _ in range(self.word_group):
                    if i < len(words):
                        display_group.append(   word := words[i])

                        # Check if the word ends with a punctuation
                        if word[-1] in self.punctuation_mapping:
                            group.append(word[:-1])
                            group.append(self.punctuation_mapping[word[-1]])
                        else:
                            group.append(word)
                        i += 1
                        if word[-1] in self.punctuation_mapping:
                            break

                highlighted_text = self.display_paragraph(paragraph, ' '.join(display_group))
                bruh = st.empty()
                bruh.text(highlighted_text)

                # self.display_paragraph(paragraph, " ".join(display_group))

                # Speak the group
                self.speak_group(" ".join(group), (is_last_group := i >= len(words)))

                # if not is_last_group:
                #     if (i // self.word_group) % self.extra_pause_frequency == 0:
                #         time.sleep(self.extra_pause_duration)

                if group[-1] == "full stop":
                    time.sleep(self.stop_after_fullstop)
                
                bruh.empty()


if __name__ == "__main__":
    st.title("dicto")

    dictator = dicto()

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="echo the string you use here")

    with open(os.path.abspath(parser.parse_args().file), "r") as t:
        text = t.read()

    try:
        dictator.dictate(text)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
