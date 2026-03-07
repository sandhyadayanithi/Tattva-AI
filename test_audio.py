from gtts import gTTS

text = "Drinking hot water cures dengue."
language = 'en'

myobj = gTTS(text=text, lang=language, slow=False)
myobj.save("test_audio.mp3")

print("Created test_audio.mp3")
