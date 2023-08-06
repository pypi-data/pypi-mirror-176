import pyaudio
import wave
import json
from os.path import dirname

def getText(text):
	res = json.loads(text)
	return res["text"]



def start():
    print("----")

    
if __name__ == '__main__':
    start()
