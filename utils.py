from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
import os
from dotenv import load_dotenv

load_dotenv()

def text_to_audio(text, audio_filename, subscription_key, region):
    """Converts text to audio and saves it to a file.

    Parameters:
    - text (str): The text to convert.
    - audio_filename (str): The name of the audio file to save.
    - subscription_key (str): Azure subscription key for Text to Speech.
    - region (str): Azure region where your Text to Speech service is hosted.
    """

    # Configure speech synthesis
    speech_config = SpeechConfig(subscription=subscription_key, region=region)
    audio_config = AudioConfig(filename=audio_filename)

    # Create a speech synthesizer
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Convert text to speech
    result = synthesizer.speak_text_async(text).get()

    # Check for successful conversion
    if result.reason == 0:  # 0 denotes failure
        raise Exception(f"Text-to-speech failed: {result.error_details}")

    print(f"Text-to-speech succeeded. Audio saved as {audio_filename}")
    
if __name__ == "__main__": 
  text = "There once used to be a Stanford sophomore named Joy. He liked saying the words indexing and based a lot. Unfortunately, he lost his voice after using a random weed pen"
  audio_filename = "test_audio.wav"
  text_to_audio(text, audio_filename, os.getenv("tts_subscription_key"), os.getenv("tts_region"))