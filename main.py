import gradio as gr
import openai, config, subprocess
import numpy as np
import os

openai.api_key = "sk-RRmdAHyCG3E29ui7IECET3BlbkFJiXKwqLEBoqiTVu5RjgP"

messages = [{"role": "system", "content": "You are a therapist."}]

def transcribe(audio):
    global messages

    audio_file= open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
    system_message = response["choices"][0]["messages"]["content"]
    print(system_message)
    messages.append({"role": "assistant", "content": system_message})

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

demo = gr.Interface(fn=transcribe,inputs=gr.Audio(source="microphone",type="filepath"),outputs="text").launch()
