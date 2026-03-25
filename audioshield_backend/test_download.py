import requests

# Humara local server address
url = "http://127.0.0.1:5000/download"

# 1. UPDATE KARO: Jo Room Code tumhe pehle mila tha (e.g., 'D95B28B4')
# Agar bhool gaye ho toh 'uploads' folder mein dekho file ka naam kya hai.
my_room_code = "0AE6B2D8" 

# 2. Wahi audio file select karo jo upload ke waqt use ki thi
files = {
    "audio": open("test.mp3", "rb") # Agar tumhari file .wav hai toh .wav likhna
}

# 3. Room code bhej rahe hain
data = {
    "room_code": my_room_code
}

print(f"Downloading file for Room: {my_room_code}... 📥")

try:
    response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        # 4. Asli file ko wapas save karo
        with open("RECOVERED_FILE.png", "wb") as f:
            f.write(response.content)
        print("✅ SUCCESS! Check your folder for 'RECOVERED_FILE.png'")
    else:
        print(f"❌ FAILED! Error: {response.json()}")

except Exception as e:
    print(f"❌ Server error: {e}")