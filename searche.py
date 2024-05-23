import speech_recognition as sr
from googlesearch import search
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
import os
import sys
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if is_admin():
        return
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Silakan berbicara...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Mengenali suara...")
        query = recognizer.recognize_google(audio, language="id-ID")
        print(f"Anda berkata: {query}")
        return query
    except sr.RequestError:
        print("Tidak dapat meminta hasil dari layanan Google Speech Recognition")
    except sr.UnknownValueError:
        print("Tidak dapat mengenali ucapan Anda")
    return None

def google_search(query, num_results=1):
    try:
        search_results = list(search(query, num_results=num_results))
        return search_results
    except Exception as e:
        print("Error:", e)
        return []

def get_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs[:5]])  # Mengambil lima paragraf pertama
        return text
    except Exception as e:
        print("Error fetching text from URL:", e)
        return "Tidak dapat mengambil teks dari URL."

def speak_text(text):
    if text:
        tts = gTTS(text=text, lang='id')
        tts.save("result.mp3")
        os.system("start result.mp3")
    else:
        print("Tidak ada teks untuk diucapkan")

def main():
    run_as_admin()
    nama = ["Projek Pencarian Suara v1.0", "by Yogi Ario"]
    for i in nama:
        print(i)
    print("\n")
    print("Pencarian ini memberikan hasil secara langsung dari Google.")
    
    while True:
        print("\nPilih metode pencarian:")
        print("1. Pencarian berdasarkan teks")
        print("2. Pencarian berdasarkan suara")
        pilihan = input("Masukkan pilihan Anda (1 atau 2, tekan enter untuk keluar): ")
        
        if pilihan == '1':
            query = input("Masukkan teks pencarian: ")
        elif pilihan == '2':
            query = recognize_speech_from_mic()
        else:
            break

        if query:
            urls = google_search(query)
            if urls:
                url = urls[0] 
                print(f"Mengambil informasi dari: {url}")
                result = get_text_from_url(url)
                print("\nHasil pencarian:\n")
                print(result)
                speak_text(result)
            else:
                print("Tidak ada hasil pencarian.")

if __name__ == "__main__":
    main()
