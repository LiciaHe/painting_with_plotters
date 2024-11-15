from google.cloud import texttospeech
import os,re


voice_option = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    name="en-US-News-L"
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def produce_tts(text,client,save_file):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_option, audio_config=audio_config
    )
    with open(f'{save_file}.mp3', "wb") as out:
        out.write(response.audio_content)

def split_text(script):
    return [s.strip() for s in re.split(r'[.!?]', script.replace('\n', ' ')) if s.strip()]

def produce_one_script(script_file_loc,client):
    with open(script_file_loc, 'r') as f:
        data=f.read()
    tag="######Scripts"
    text =data[data.index(tag)+len(tag):]
    script_by_line=split_text(text)
    for i,line in enumerate(script_by_line):
        print(i,line)
        produce_tts(
            line,
            client,
            f'{save_address}tts_{i}'
        )
base_addr="D:\licia\code\Painting_With_Plotters/"

save_address=f'{base_addr}assets/local/exclude/0/'
mkdir(save_address)
client=texttospeech.TextToSpeechClient()
produce_one_script(
    f'{base_addr}Note/0_Introduction_To_Plotter_Painting.md',
    client
)

