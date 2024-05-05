from tkinter import Tk, Toplevel, Button, Label, filedialog, Frame
from tkinter.ttk import Style
import TrichRutDacTrung as ft
import jsonpickle as json
import TinhDoTuongDongTest
import threading
import sounddevice as sd
import soundfile as sf

# Mở file JSON và đọc nội dung của file
with open('metadata/data.json', 'r') as file:
    json_data = file.read()

# Chuyển đổi nội dung file JSON thành đối tượng Python
clusters = json.loads(json_data)

# Hàm để phát file âm thanh
def play_sound(file_path):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()

# Hàm để tạo một thread để phát âm thanh
def play_sound_threaded(file_path):
    thread = threading.Thread(target=play_sound, args=(file_path,))
    thread.start()

def clear_widgets(parent):
    for widget in parent.winfo_children():
        widget.destroy()

def nhanDang():
    file = filedialog.askopenfilename(filetypes = (("Audio files","*.wav"),("all files","*.*")))
    
    if file:
        clear_widgets(frame) # Xóa các widget hiện có trong frame
        features = ft.features(file=file)
        links = TinhDoTuongDongTest.SimilarityCalculation(clusters=clusters, features=features)
        meg = 'Ba File âm thanh tiếng chim có độ tương đồng gần nhất: '
        lbl1 = Label(frame, text=meg, font=("Arial Bold", 14), anchor="sw", wraplength=400)
        lbl1.pack(pady=10)
        print(features)
        for link in links:
            link = link.replace('\\', '/')
            butSound = Button(frame, text=link, command=lambda link=link: play_sound_threaded(link))
            butSound.pack(pady=5)
        # Thêm nút cho file được chọn
        butSelectedFile = Button(frame, text="Play Selected File", command=lambda: play_sound_threaded(file))
        butSelectedFile.pack(pady=5)

window = Tk()
window.title("NHẬN DẠNG ÂM THANH TIẾNG CHIM")
window.geometry('800x600')

frame = Frame(window)
frame.pack(pady=10)

butAdd = Button(window, text='Chọn tệp âm thanh', width=20, height=2, command=nhanDang)
butAdd.pack(pady=10)

window.mainloop()
