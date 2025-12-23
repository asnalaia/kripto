import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from stegano import lsb

class SecurityIntegrator:
    def __init__(self):
        self.block_size = AES.block_size
    
    def generate_aes_key(self):
        """Membuat kunci AES acak 32 bytes (256 bit)."""
        return get_random_bytes(32)

    def encrypt_data_aes(self, plain_text, key):
        """
        Mengenkripsi teks biasa menjadi AES Ciphertext.
        Output dikembalikan dalam format Base64 String agar mudah diproses Stegano.
        """
        if isinstance(plain_text, str):
            data_bytes = plain_text.encode('utf-8')
        else:
            data_bytes = plain_text

        cipher = AES.new(key, AES.MODE_CBC)
        
        ciphertext_bytes = cipher.encrypt(pad(data_bytes, self.block_size))
        
        combined_data = cipher.iv + ciphertext_bytes
        
        return base64.b64encode(combined_data).decode('utf-8')

    def decrypt_data_aes(self, encrypted_string, key):
        """
        Mengembalikan teks asli dari AES Ciphertext (Base64 String).
        """
        try:
            combined_data = base64.b64decode(encrypted_string)

            iv = combined_data[:16]
            ciphertext = combined_data[16:]
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(ciphertext), self.block_size)
            
            return decrypted_data.decode('utf-8')
        except Exception as e:
            return f"Error Decrypting: {str(e)}"

    def hide_secret_in_image(self, secret_message, cover_image_path, output_path):
        """
        Menyembunyikan string rahasia ke dalam gambar menggunakan LSB.
        secret_message: Harus berupa string (hasil dari encrypt_data_aes).
        """
        try:
            print(f"[*] Sedang menyembunyikan data ke {cover_image_path}...")
            secret_image = lsb.hide(cover_image_path, secret_message)
            secret_image.save(output_path)
            print(f"[+] Sukses! Gambar steganografi disimpan di: {output_path}")
            return True
        except Exception as e:
            print(f"[-] Gagal menyembunyikan data: {str(e)}")
            return False

    def extract_secret_from_image(self, stego_image_path):
        """
        Mengambil string rahasia dari gambar steganografi.
        """
        try:
            print(f"[*] Sedang mengekstrak data dari {stego_image_path}...")
            secret_message = lsb.reveal(stego_image_path)
            return secret_message
        except Exception as e:
            print(f"[-] Gagal ekstrak data: {str(e)}")
            return None

if __name__ == "__main__":
    engine = SecurityIntegrator()

    pesan_rahasia = "Halo, ini adalah data rahasia Asnawati untuk Skripsi!"
    kunci_aes = engine.generate_aes_key()
    
    print(f"Pesan Asli: {pesan_rahasia}")

    encrypted_msg = engine.encrypt_data_aes(pesan_rahasia, kunci_aes)
    print(f"Terenskripsi (AES Base64): {encrypted_msg[:20]}...") 

    input_img = "sample_image.png" 
    output_img = "secret_image.png"

    if os.path.exists(input_img):
        engine.hide_secret_in_image(encrypted_msg, input_img, output_img)
        
        extracted_msg = engine.extract_secret_from_image(output_img)
        final_result = engine.decrypt_data_aes(extracted_msg, kunci_aes)
        
        print(f"Hasil Akhir (Decrypted): {final_result}")
    else:
        print(f"[!] Warning: Tidak ditemukan '{input_img}'. Siapkan gambar JPG dulu untuk tes stegano.")