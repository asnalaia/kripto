import hashlib

def hitung_hash(nama_file):
    sha256 = hashlib.sha256()
    with open(nama_file, "rb") as f:
        while True:
            data = f.read(65536)
            if not data: break
            sha256.update(data)
    return sha256.hexdigest()

# Bandingkan gambar asli dan hasil stego
hash1 = hitung_hash("sample_image.png")
hash2 = hitung_hash("secret_image.png")

print(f"Sidik Jari Gambar Asli : {hash1}")
print(f"Sidik Jari Gambar Stego: {hash2}")

if hash1 != hash2:
    print("\n[KESIMPULAN] File BERBEDA secara digital! (Ada data tersembunyi)")
else:
    print("\n[KESIMPULAN] File SAMA PERSIS (Gagal menyembunyikan data)")