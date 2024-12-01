import speech_recognition as sr

def speech2text(q):
    print("started")
    phrases = ["catapult", "ram", "build", "south", "east", "west", "north"]
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = "C:\\Users\\Jonathan Boilard\\Documents\\keys\\speech-to-text-372021-5e837ec9574e.json"
    r = sr.Recognizer()
    r.pause_threshold = 0.25
    r.non_speaking_duration = 0.25
    text = ""

    try:
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=2, phrase_time_limit=5)
        text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, preferred_phrases=phrases)
        with open('sentences.txt', 'a') as f:
            f.write(f"{text}\n")
        q.put(text)
        
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))      
    except Exception as e:
        print("another error: {0}".format(e))
        
    

    
    
    