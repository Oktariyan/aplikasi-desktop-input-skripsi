from PIL import Image
import os

def create_ico():
    try:
        # Pastikan logo_unair.png ada di folder assets
        img = Image.open('assets/logo_unair.png')
        
        # Simpan ICO di folder utama
        ico_path = 'assets/logo_unair.ico'
        img.save(ico_path, sizes=[(256,256), (128,128), (64,64), (32,32)])
        print(f"File ICO berhasil dibuat di {ico_path}")
        return True
    except Exception as e:
        print(f"Error membuat ICO: {str(e)}")
        return False

if __name__ == "__main__":
    create_ico()