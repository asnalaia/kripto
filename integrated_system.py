import base64
import json
import os
from typing import Tuple

# Import dari file asli teman (TIDAK DIUBAH)
from rsa_manager import RSAManager
from hello import SecurityIntegrator


class IntegratedSecuritySystem:
    """
    Wrapper class yang mengintegrasikan kode teman dengan alur yang benar.
    
    ALUR LENGKAP:
    =============
    ENKRIPSI:
    1. Digital Signature → sign plaintext dengan private key
    2. Gabungkan plaintext + signature
    3. AES Encryption → encrypt dengan AES
    4. RSA Key Encryption → encrypt AES key dengan RSA
    5. LSB Steganography → hide dalam gambar
    
    DEKRIPSI:
    1. Extract dari gambar
    2. Decrypt AES key dengan RSA
    3. Decrypt ciphertext dengan AES
    4. Pisahkan plaintext dan signature
    5. Verify signature
    6. Return plaintext
    """
    
    def __init__(self, 
                 sender_private_key_path="private_key.pem", 
                 sender_public_key_path="public_key.pem",
                 receiver_public_key_path="public_key.pem",
                 receiver_private_key_path="private_key.pem"):
        """
        Initialize dengan menggunakan class asli dari teman
        """
        # Gunakan class asli dari rsa_manager.py (TIDAK DIUBAH)
        self.rsa_mgr = RSAManager(
            private_key_path=sender_private_key_path,
            public_key_path=sender_public_key_path
        )
        
        # Gunakan class asli dari hello.py (TIDAK DIUBAH)
        self.security = SecurityIntegrator()
        
        # Store key paths
        self.sender_private_key_path = sender_private_key_path
        self.sender_public_key_path = sender_public_key_path
        self.receiver_public_key_path = receiver_public_key_path
        self.receiver_private_key_path = receiver_private_key_path
        
        # Ensure keys exist
        self._ensure_keys_exist()
    
    def _ensure_keys_exist(self):
        """Generate keys jika belum ada"""
        if not os.path.exists(self.sender_private_key_path):
            print("[*] Generating RSA keys...")
            from Crypto.PublicKey import RSA
            key = RSA.generate(2048)
            
            with open(self.sender_private_key_path, 'wb') as f:
                f.write(key.export_key())
            with open(self.sender_public_key_path, 'wb') as f:
                f.write(key.publickey().export_key())
            
            print("[✓] Keys generated")
        else:
            print("[✓] Keys already exist")
    
    def encrypt_and_hide(self, plaintext_file_path: str, cover_image_path: str, 
                         output_image_path: str) -> Tuple[bool, str]:
        """
        Proses lengkap enkripsi dan hiding menggunakan KODE ASLI TEMAN
        """
        try:
            print("\n" + "="*60)
            print("MEMULAI PROSES ENKRIPSI")
            print("="*60)
            
            # STEP 1: Baca plaintext
            with open(plaintext_file_path, 'rb') as f:
                plaintext = f.read()
            print(f"[1] ✓ Plaintext dimuat: {len(plaintext)} bytes")
            
            # STEP 2: Digital Signature (menggunakan rsa_manager.py asli)
            private_key = self.rsa_mgr.load_private_key()
            signature = self.rsa_mgr.sign_data(plaintext, private_key)
            print(f"[2] ✓ Digital signature dibuat")
            
            # STEP 3: Gabungkan plaintext + signature
            combined = json.dumps({
                'data': base64.b64encode(plaintext).decode('utf-8'),
                'signature': signature
            })
            print(f"[3] ✓ Data digabungkan dengan signature")
            
            # STEP 4: AES Encryption (menggunakan hello.py asli)
            aes_key = self.security.generate_aes_key()
            
            # hello.py return Base64 STRING (bukan bytes!)
            ciphertext_b64_string = self.security.encrypt_data_aes(combined, aes_key)
            
            print(f"[4] ✓ Data dienkripsi dengan AES")
            
            # STEP 5: RSA Key Encryption (menggunakan rsa_manager.py asli)
            public_key = self.rsa_mgr.load_public_key()
            encrypted_aes_key = self.rsa_mgr.encrypt_aes_key_with_rsa(aes_key, public_key)
            print(f"[5] ✓ Kunci AES dienkripsi dengan RSA")
            
            # STEP 6: Gabungkan ciphertext + encrypted key
            payload = json.dumps({
                'ciphertext': ciphertext_b64_string,  # Sudah Base64 string
                'encrypted_key': encrypted_aes_key
            })
            print(f"[6] ✓ Payload final disiapkan: {len(payload)} karakter")
            
            # STEP 7: LSB Steganography (menggunakan hello.py asli)
            success = self.security.hide_secret_in_image(
                payload,
                cover_image_path,
                output_image_path
            )
            
            if success:
                print(f"[7] ✓ Data berhasil disembunyikan dalam gambar!")
                print("="*60)
                return True, f"Enkripsi berhasil!\nStego image: {output_image_path}"
            else:
                return False, "Gagal menyembunyikan data dalam gambar"
                
        except FileNotFoundError as e:
            return False, f"File tidak ditemukan: {str(e)}"
        except Exception as e:
            return False, f"Error saat enkripsi: {str(e)}"
    
    def extract_and_decrypt(self, stego_image_path: str, output_file_path: str) -> Tuple[bool, str]:
        """
        Proses lengkap extraction dan dekripsi menggunakan KODE ASLI TEMAN
        """
        try:
            print("\n" + "="*60)
            print("MEMULAI PROSES DEKRIPSI")
            print("="*60)
            
            # STEP 1: Extract dari gambar (menggunakan hello.py asli)
            payload_json = self.security.extract_secret_from_image(stego_image_path)
            if not payload_json:
                return False, "Tidak ada data tersembunyi dalam gambar"
            print(f"[1] ✓ Data diekstrak dari gambar")
            
            # STEP 2: Parse payload
            payload = json.loads(payload_json)
            ciphertext_b64_string = payload['ciphertext']  # Ini Base64 string
            encrypted_aes_key = payload['encrypted_key']
            print(f"[2] ✓ Payload diparsing")
            
            # STEP 3: Decrypt AES key (menggunakan rsa_manager.py asli)
            private_key = self.rsa_mgr.load_private_key()
            aes_key = self.rsa_mgr.decrypt_aes_key_with_rsa(encrypted_aes_key, private_key)
            print(f"[3] ✓ Kunci AES didekripsi")
            
            # STEP 4: Decrypt ciphertext (menggunakan hello.py asli)
            print(f"[DEBUG] Ciphertext (Base64) length: {len(ciphertext_b64_string)}")
            print(f"[DEBUG] AES Key length: {len(aes_key)} bytes")
            
            # hello.py expect Base64 STRING input
            combined_json = self.security.decrypt_data_aes(ciphertext_b64_string, aes_key)
            
            # Check if decryption failed
            if isinstance(combined_json, str) and combined_json.startswith("Error Decrypting"):
                print(f"[DEBUG] Decryption error: {combined_json}")
                return False, f"Dekripsi gagal: {combined_json}"
            
            print(f"[DEBUG] Decrypted data (first 200 chars): {combined_json[:200]}")
            print(f"[4] ✓ Ciphertext didekripsi")
            
            # STEP 5: Pisahkan plaintext dan signature
            combined = json.loads(combined_json)
            plaintext = base64.b64decode(combined['data'])
            signature = combined['signature']
            print(f"[5] ✓ Plaintext dan signature dipisahkan")
            
            # STEP 6: Verify signature (menggunakan rsa_manager.py asli)
            public_key = self.rsa_mgr.load_public_key()
            is_valid = self.rsa_mgr.verify_signature(plaintext, signature, public_key)
            
            if not is_valid:
                print(f"[6] ✗ Signature verification FAILED!")
                print("="*60)
                return False, "⚠️ PERINGATAN: Signature tidak valid!\nData mungkin corrupt!"
            
            print(f"[6] ✓ Signature berhasil diverifikasi")
            
            # STEP 7: Save plaintext
            with open(output_file_path, 'wb') as f:
                f.write(plaintext)
            print(f"[7] ✓ Plaintext disimpan ke: {output_file_path}")
            print("="*60)
            
            return True, f"Dekripsi berhasil!\n✓ Signature valid\nFile: {output_file_path}"
            
        except FileNotFoundError as e:
            return False, f"File tidak ditemukan: {str(e)}"
        except json.JSONDecodeError as e:
            return False, f"Data corrupt atau format JSON tidak valid: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"


# ============================================================================
# TESTING
# ============================================================================

def test_system():
    """Test integrated system"""
    print("\n" + "="*70)
    print(" "*15 + "🔐 TESTING INTEGRATED SYSTEM 🔐")
    print("="*70)
    
    system = IntegratedSecuritySystem()
    
    # Create test file
    test_data = "Ini adalah data rahasia untuk skripsi Asnawati & Virginia! 🔒"
    os.makedirs("test_files", exist_ok=True)
    
    with open("test_files/secret.txt", "w", encoding="utf-8") as f:
        f.write(test_data)
    print("\n[*] Test file created: test_files/secret.txt")
    
    # Check sample image
    if not os.path.exists("test_images/sample_image.png"):
        print("\n⚠️  WARNING: test_images/sample_image.png not found!")
        print("Please prepare a cover image first.")
        return
    
    # Test encryption
    print("\n" + "🔒 FASE ENKRIPSI ".ljust(70, "="))
    success, msg = system.encrypt_and_hide(
        plaintext_file_path="test_files/secret.txt",
        cover_image_path="test_images/sample_image.png",
        output_image_path="secret_stego.png"
    )
    
    if not success:
        print(f"\n❌ ENKRIPSI GAGAL: {msg}")
        return
    
    print(f"\n✅ {msg}")
    
    # Test decryption
    print("\n" + "🔓 FASE DEKRIPSI ".ljust(70, "="))
    success, msg = system.extract_and_decrypt(
        stego_image_path="secret_stego.png",
        output_file_path="test_files/recovered.txt"
    )
    
    if not success:
        print(f"\n❌ DEKRIPSI GAGAL: {msg}")
        return
    
    print(f"\n✅ {msg}")
    
    # Verify
    with open("test_files/recovered.txt", "r", encoding="utf-8") as f:
        recovered = f.read()
    
    print("\n" + "="*70)
    print(" "*25 + "HASIL VERIFIKASI")
    print("="*70)
    print(f"\nOriginal : {test_data}")
    print(f"Recovered: {recovered}")
    print(f"\n{'✅ MATCH' if recovered == test_data else '❌ MISMATCH'}")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_system()