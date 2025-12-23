import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from aes_stego_manager import SecurityIntegrator


def calculate_psnr_mse(image_path_original, image_path_stego):
    """Menghitung nilai MSE dan PSNR untuk Paper Bab Result."""
    img1 = cv2.imread(image_path_original)
    img2 = cv2.imread(image_path_stego)
    
    if img1 is None or img2 is None:
        return "Error", "Error"

    mse = np.mean((img1 - img2) ** 2)
    
    if mse == 0:
        psnr = 100
    else:
        PIXEL_MAX = 255.0
        psnr = 20 * np.log10(PIXEL_MAX / np.sqrt(mse))
        
    return mse, psnr

def generate_histogram(image_path, title, output_file):
    """Membuat grafik Histogram RGB untuk Paper."""
    img = cv2.imread(image_path)
    colors = ('b', 'g', 'r')
    
    plt.figure()
    plt.title(f"Histogram: {title}")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    
    for i, color in enumerate(colors):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
        
    plt.savefig(output_file)
    plt.close()
    print(f"[+] Grafik Histogram disimpan: {output_file}")

def speed_test(engine, file_size_kb):
    """Mengukur kecepatan enkripsi."""
    dummy_data = "A" * (1024 * file_size_kb)
    key = engine.generate_aes_key()
    
    start_time = time.time()
    engine.encrypt_data_aes(dummy_data, key)
    end_time = time.time()
    
    duration = end_time - start_time
    return duration

if __name__ == "__main__":
    engine = SecurityIntegrator()
    
    cover_img = "sample_image.png" 
    stego_img = "result_for_paper.png"
    
    if not os.path.exists(cover_img):
        print(f"[!] Error: Tolong sediakan gambar {cover_img} dulu!")
        exit()

    print("\n[1] Membuat Sampel Data (Enkripsi & Hide)...")
    pesan_rahasia = "Data ini untuk keperluan paper" * 50
    kunci = engine.generate_aes_key()
    
    cipher = engine.encrypt_data_aes(pesan_rahasia, kunci)
    engine.hide_secret_in_image(cipher, cover_img, stego_img)
    
    print("\n[2] Menghitung MSE & PSNR...")
    mse_val, psnr_val = calculate_psnr_mse(cover_img, stego_img)
    print(f"   >>> MSE  : {mse_val:.4f} (Makin kecil makin bagus)")
    print(f"   >>> PSNR : {psnr_val:.4f} dB (Di atas 40dB itu sangat bagus)")
    
    print("\n[3] Generate Grafik Histogram...")
    generate_histogram(cover_img, "Cover Image (Original)", "hist_original.png")
    generate_histogram(stego_img, "Stego Image (Hidden Data)", "hist_stego.png")
    
    print("\n[4] Benchmark Kecepatan Enkripsi (AES)...")
    sizes = [100, 500, 1000] # dalam KB
    for size in sizes:
        waktu = speed_test(engine, size)
        print(f"   >>> Ukuran {size} KB : {waktu:.5f} detik")

    print("\n selesai.")