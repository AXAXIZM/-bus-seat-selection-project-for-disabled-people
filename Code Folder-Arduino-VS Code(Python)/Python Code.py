import serial
import time
from tkinter import *


ser = serial.Serial('COM10', 9600) 

# yetkili oln UID
authorizedUID = ("Yetkili olan ve arduino kod bloğundan edindiğimiz kart UID")


seat_status = { f'A{i}': False for i in range(1, 13) }  # 12 koltuk


selections = {}

# Tkinter GUI 
def start_seat_selection(uid):
    window = Tk()
    window.title("Koltuk Seçim Ekranı")
    window.geometry("500x500")
    window.config(bg="lightgray")

    #uyarı 
    
    message_label = Label(window, text="", fg="red", font=("Arial", 12))
    message_label.grid(row=0, column=0, columnspan=4, pady=10)

    #Bilgilendirme 
    info_label = Label(window, text="Lütfen koltuk seçin.", fg="blue", font=("Arial", 12))
    info_label.grid(row=1, column=0, columnspan=4, pady=5)

    # Son seçilen koltuğun ismini takip etmek için bir değişken
    temp_selected_seat = None  # Geçici seçim

    def seat_selected(seat_number, button):
        nonlocal temp_selected_seat

        # Eğer geçici olarak başka bir koltuk seçildiyse öncekini yeşile döndür
        if temp_selected_seat and temp_selected_seat != seat_number:
            buttons[temp_selected_seat].config(bg='green')  # Önceki geçici koltuğu yeşil yap

        # Bu koltuğa tıklanmısa bu koltuğu geçci olarak işaretle
        if not seat_status[seat_number]:  # Koltuk boşsa
            temp_selected_seat = seat_number  # Geçici olarak seçilen koltuğu güncelle
            button.config(bg='red')  # Seçilen koltuğu kırmızıya döndür
            info_label.config(text=f"Koltuk {seat_number} seçildi. Seçiminizi tamamlamak için 'Tamam' butonuna basın.")
        else:
            message_label.config(text=f"Koltuk {seat_number} zaten seçilmiş.")
            info_label.config(text=f"Koltuk {seat_number} zaten dolu. Lütfen başka bir koltuk seçin.")

    # Koltuk seçeneklerini buton olarak ekleme
    seats = [f'A{i}' for i in range(1, 13)]
    buttons = {}

    # Koltuk durumlarına göre renkleri güncelleme
    def update_seat_colors():
        for seat, button in buttons.items():
            if seat_status[seat]:
                button.config(bg='red')  # Eğer koltuk doluysa kırmızı
            else:
                button.config(bg='green')  # Eğer bossa yeşil

    # Koltukları bir grid düzeninde gösterelim (3 satır, 4 sütun)
    row, col = 2, 0  # Koltuklar için grid yerleşimi başlatma
    for seat in seats:
        button = Button(window, text=f"Koltuk {seat}", width=10, height=3, font=("Arial", 10, "bold"), relief="solid")
        button.grid(row=row, column=col, padx=10, pady=10)
        buttons[seat] = button
        # Butonlara tıklanınca seat_selected fonksiyonu çalışacak
        button.config(command=lambda seat=seat, button=button: seat_selected(seat, button))

        col += 1
        if col == 4:  # 4. sütuna gelince bir alt satıra geç
            col = 0
            row += 1

    # Koltuk renklerini güncelle
    update_seat_colors()

    # "Tamam" butonu ekliyoruz
    def finish_selection():
        nonlocal temp_selected_seat
        if temp_selected_seat:
            message_label.config(text=f"Seçiminiz tamamlandı! Seçilen Koltuk: {temp_selected_seat}")
            seat_status[temp_selected_seat] = True  # Koltuğu dolu yap
            selections[uid] = temp_selected_seat  # Kart UID'sine koltuk numarasını kaydet
            info_label.config(text=f"Seçiminiz tamamlandı! Koltuk {temp_selected_seat} seçildi.")
        else:
            message_label.config(text="Henüz bir koltuk seçilmedi.")
            info_label.config(text="Lütfen bir koltuk seçin.")
        print(f"Seçiminiz tamamlandı! Seçilen Koltuk: {temp_selected_seat}")
        window.destroy()  # Seçim tamamlanınca pencereyi kapat

    finish_button = Button(window, text="Tamam", command=finish_selection, width=20, height=2, font=("Arial", 12, "bold"))
    finish_button.grid(row=row+1, column=0, columnspan=4, pady=20)

    window.mainloop()

# RFID kart okuma ve koltuk seçimi tetikleme
while True:
    if ser.in_waiting > 0:  # Arduino'dan veri varsa
        uid = ser.readline().decode('utf-8').strip()  # Arduino'dan gelen UID verisini oku
        print(f"Okunan UID: {uid}")

        if uid == authorizedUID:
            # Yolcu kartını okuttuğunda koltuk seçimi yapılacak
            start_seat_selection(uid)

        else:
            print("Erişim reddedildi. Yetkisiz kart.")

    time.sleep(1)
