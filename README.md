# dicto.py 📝🔊

This is your friendly dictation companion, designed to make writing tasks a breeze!

dicto.py is a simple yet powerful application that reads text aloud, allowing you to write it down physically at your own pace. It's perfect for:

- Students who want to practice their handwriting while studying
- Typewriters looking to increase their efficiency
- Anyone who prefers a hands-on approach to note-taking

## Features

- 🌐 Web-based interface powered by Streamlit
- 🎙️ Text-to-speech functionality using gTTS
- 🌍 Multiple language support 
- 🗣️ Accent selection (UK, Nigerian, Australian so far)
- ⏩ Customizable speech rate and pauses
- 🔴 Real-time text highlighting
- 📤 Upload your own text files or use the text area

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/moiSentineL/dicto.git
   ```

2. Navigate to the project directory:
   ```
   cd dicto
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run dicto.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the web interface to:
   - Enter text in the text area or upload a `.txt` file
   - Configure dictation settings in the sidebar:
     - Select language and accent
     - Adjust pause duration after full stops
     - Set the number of words to read at once
     - Modify the minimum pause and length multiplier
   - Click the "Dictate!" button to start the dictation

## Configuration Options

- **Language**: Choose between English, French, and Hindi
- **Accent**: Select UK, Nigerian, or Australian accent
- **Pause after fullstop**: Set the duration of pause after each full stop (0-5 seconds)
- **Word Groups**: Choose how many words to read in each group (0-5 words)
- **Minimum pause**: Set the minimum pause between word groups (0-3 seconds)
- **Length Multiplier**: Adjust the pause duration based on word length (0x-1x)

## How It Works

1. Dicto processes the input text, breaking it into paragraphs and word groups.
2. It uses gTTS (Google Text-to-Speech) to convert text to speech.
3. The application highlights the current word group being read.
4. Pygame is used to play the audio.
5. Customizable pauses are inserted between word groups and after punctuation marks.

## Contributing

We welcome contributions! If you have ideas for improvements or bug fixes, please open an issue or submit a pull request.

## Support
If you find Dicto.py helpful, ~~consider buying the developer a coffee! ☕~~ just make sure you have fun with it and share it with others who might benefit!.

Also maybe check out some of my other [stuff](https://github.com/moisentinel) 👈

Happy writing! ✍️