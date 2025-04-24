import sys
from Adafruit_IO import MQTTClient
from transformers import pipeline
import time
import sounddevice as sd
import scipy.io.wavfile as wav

# ----------- CẤU HÌNH ADAFRUIT -------------
AIO_FEED_ID = "AI"
AIO_USERNAME = "add nam"   
AIO_KEY = "add key"         

# ----------- KẾT NỐI MQTT -------------
def connected(client):
    print("Kết nối thành công!")
    client.subscribe(AIO_FEED_ID)

def subscribe(client, userdata, mid, granted_qos):
    print("Đã subscribe tới feed:", AIO_FEED_ID)

def disconnected(client):
    print("Mất kết nối với Adafruit IO.")
    sys.exit(1)

def message(client, feed_id, payload):
    print(f"Nhận dữ liệu từ Adafruit: {payload}")

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

# ----------- MÔ HÌNH NHẬN DẠNG GIỌNG NÓI -------------
transcriber = pipeline(
    "automatic-speech-recognition",
    model="vinai/PhoWhisper-small",
    device=-1
)
def record_audio(filename="audio.wav", duration=10, samplerate=16000):
    print(f" Đang ghi âm trong {duration} giây...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, samplerate, recording)
    print(f" Ghi âm xong. Lưu tại: {filename}")

def transcribe(filename="audio.wav"):
    print(" Đang xử lý âm thanh...")
    result = transcriber(filename)
    text = result["text"].lower()
    print(" Văn bản nhận được:", text)
    return text

# ----------- XỬ LÝ ĐIỀU KHIỂN -------------
def handle_command(text):
    if "bật" in text and "máy bơm" in text:
        print("Lệnh: BẬT máy bơm")
        client.publish(AIO_FEED_ID, "on")
    elif "tắt" in text and "máy bơm" in text:
        print("Lệnh: TẮT máy bơm")
        client.publish(AIO_FEED_ID, "off")
    else:
        print("Không nhận diện được lệnh phù hợp.")

# ----------- MAIN -------------
if __name__ == "__main__":
    record_audio("audio.wav", duration=5)
    text = transcribe("output1.wav")
    handle_command(text)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🔌 Đã ngắt kết nối.")
# from pydub import AudioSegment

# # Đọc file AAC
# audio = AudioSegment.from_file("2.aac", format="aac")

# # Xuất ra WAV 
# audio.export("output1.wav", format="wav")

# print("✅ Đã chuyển AAC thành WAV")
