"""
gui_cryptostego.py
====================================
GUI Application for Integrated Cryptography and Steganography System
"""

try:
    from integrated_system import IntegratedSecuritySystem
    from rsa_manager import RSAManager
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    from pathlib import Path
    from PIL import Image, ImageTk  # ← TAMBAHKAN INI
    import os  # ← Pastikan ini juga ada
except ImportError as e:
    print(f"ERROR: {str(e)}")
    print("Pastikan file ada:")
    print("- rsa_manager.py")
    print("- hello.py") 
    print("- integrated_system.py")
    print("- Pillow library (pip install pillow)")
    exit(1)


class CryptoStegoGUI:
    """
    GUI Application untuk Sistem Kriptografi dan Steganografi Terintegrasi
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Secure File Steganography System - Kelompok 5")
        self.root.geometry("950x750")
        self.root.resizable(False, False)
        
        # Styling colors
        self.bg_color = "#f5f5f5"
        self.accent_color = "#1976D2"
        self.success_color = "#4CAF50"
        self.error_color = "#F44336"
        self.dark_color = "#212121"
        
        self.root.configure(bg=self.bg_color)
        
        # Variables
        self.plaintext_file_path = tk.StringVar()
        self.cover_image_path = tk.StringVar()
        self.stego_image_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        
        self.cover_image_preview = None
        self.stego_image_preview = None
        
        # Initialize crypto system
        self.setup_crypto_system()
        
        # Build UI
        self.build_ui()
    
    def setup_crypto_system(self):
        """Initialize cryptography system"""
        try:
            # Setup paths (menggunakan keys yang sudah ada)
            self.sender_private = "private_key.pem"
            self.sender_public = "public_key.pem"
            self.receiver_private = "private_key.pem"
            self.receiver_public = "public_key.pem"
            
            # Initialize system
            self.crypto_system = IntegratedSecuritySystem(
                sender_private_key_path=self.sender_private,
                sender_public_key_path=self.sender_public,
                receiver_public_key_path=self.receiver_public,
                receiver_private_key_path=self.receiver_private
            )
            
            print("[✓] Crypto system initialized")
            
        except Exception as e:
            messagebox.showerror("Initialization Error", 
                               f"Gagal inisialisasi crypto system:\n{str(e)}")
            self.root.quit()
    
    def build_ui(self):
        """Build complete user interface"""
        
        # ========== HEADER ==========
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=70)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            header_frame,
            text="🔐 Secure File Steganography System",
            font=("Segoe UI", 20, "bold"),
            bg=self.accent_color,
            fg="white",
            pady=20
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Cryptography + Steganography Integration | Kelompok 5",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg="white"
        )
        subtitle_label.pack()
        
        # ========== NOTEBOOK (TABS) ==========
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Configure tab style
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 11, 'bold'))
        
        # Tab 1: Encryption & Hiding
        self.encrypt_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.encrypt_frame, text="  🔒 Encrypt & Hide  ")
        self.build_encrypt_tab()
        
        # Tab 2: Extraction & Decryption
        self.decrypt_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.decrypt_frame, text="  🔓 Extract & Decrypt  ")
        self.build_decrypt_tab()
        
        # ========== STATUS BAR ==========
        self.status_bar = tk.Label(
            self.root,
            text="Ready | RSA Keys: Loaded ✓",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="white",
            font=("Segoe UI", 9),
            padx=10,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def build_encrypt_tab(self):
        """Build encryption and hiding interface"""
        
        # ========== SECTION 1: Select Secret File ==========
        file_section = tk.LabelFrame(
            self.encrypt_frame,
            text="  1️⃣  Select Secret File  ",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_color,
            fg=self.dark_color,
            padx=20,
            pady=15
        )
        file_section.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            file_section,
            text="Pilih file yang ingin dienkripsi dan disembunyikan:",
            bg=self.bg_color,
            font=("Segoe UI", 10),
            fg=self.dark_color
        ).pack(anchor=tk.W)
        
        file_frame = tk.Frame(file_section, bg=self.bg_color)
        file_frame.pack(fill=tk.X, pady=8)
        
        file_entry = tk.Entry(
            file_frame,
            textvariable=self.plaintext_file_path,
            width=65,
            state='readonly',
            font=("Consolas", 10),
            relief=tk.SOLID,
            bd=1
        )
        file_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        
        tk.Button(
            file_frame,
            text="📁 Select File",
            command=self.select_plaintext_file,
            bg=self.accent_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=5
        ).pack(side=tk.LEFT)
        
        # ========== SECTION 2: Select Cover Image ==========
        image_section = tk.LabelFrame(
            self.encrypt_frame,
            text="  2️⃣  Select Cover Image (PNG/JPG)  ",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_color,
            fg=self.dark_color,
            padx=20,
            pady=15
        )
        image_section.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            image_section,
            text="Pilih gambar untuk menyembunyikan data rahasia:",
            bg=self.bg_color,
            font=("Segoe UI", 10),
            fg=self.dark_color
        ).pack(anchor=tk.W)
        
        image_frame = tk.Frame(image_section, bg=self.bg_color)
        image_frame.pack(fill=tk.X, pady=8)
        
        image_entry = tk.Entry(
            image_frame,
            textvariable=self.cover_image_path,
            width=65,
            state='readonly',
            font=("Consolas", 10),
            relief=tk.SOLID,
            bd=1
        )
        image_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        
        tk.Button(
            image_frame,
            text="🖼️  Select Image",
            command=self.select_cover_image,
            bg=self.accent_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=5
        ).pack(side=tk.LEFT)
        
        # Image Preview
        self.cover_preview_label = tk.Label(
            image_section,
            text="No image selected\n\nKlik 'Select Image' untuk memilih gambar",
            bg="white",
            width=55,
            height=8,
            relief=tk.SUNKEN,
            font=("Segoe UI", 10),
            fg="gray"
        )
        self.cover_preview_label.pack(pady=10)
        
        # ========== ACTION SECTION ==========
        action_section = tk.Frame(self.encrypt_frame, bg=self.bg_color)
        action_section.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(
            action_section,
            text="🚀 Encrypt and Hide in Image",
            command=self.encrypt_and_hide,
            bg=self.success_color,
            fg="white",
            font=("Segoe UI", 14, "bold"),
            height=2,
            cursor="hand2",
            relief=tk.FLAT
        ).pack(fill=tk.X)
    
    def build_decrypt_tab(self):
        """Build extraction and decryption interface"""
        
        # ========== SECTION 1: Select Stego Image ==========
        stego_section = tk.LabelFrame(
            self.decrypt_frame,
            text="  1️⃣  Select Stego Image  ",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_color,
            fg=self.dark_color,
            padx=20,
            pady=15
        )
        stego_section.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            stego_section,
            text="Pilih gambar yang berisi data tersembunyi:",
            bg=self.bg_color,
            font=("Segoe UI", 10),
            fg=self.dark_color
        ).pack(anchor=tk.W)
        
        stego_frame = tk.Frame(stego_section, bg=self.bg_color)
        stego_frame.pack(fill=tk.X, pady=8)
        
        stego_entry = tk.Entry(
            stego_frame,
            textvariable=self.stego_image_path,
            width=65,
            state='readonly',
            font=("Consolas", 10),
            relief=tk.SOLID,
            bd=1
        )
        stego_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        
        tk.Button(
            stego_frame,
            text="🖼️  Select Stego Image",
            command=self.select_stego_image,
            bg=self.accent_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=5
        ).pack(side=tk.LEFT)
        
        # Stego Image Preview
        self.stego_preview_label = tk.Label(
            stego_section,
            text="No image selected\n\nKlik 'Select Stego Image' untuk memilih gambar",
            bg="white",
            width=55,
            height=8,
            relief=tk.SUNKEN,
            font=("Segoe UI", 10),
            fg="gray"
        )
        self.stego_preview_label.pack(pady=10)
        
        # ========== SECTION 2: Output File ==========
        output_section = tk.LabelFrame(
            self.decrypt_frame,
            text="  2️⃣  Save Decrypted File As  ",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_color,
            fg=self.dark_color,
            padx=20,
            pady=15
        )
        output_section.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            output_section,
            text="Tentukan lokasi penyimpanan file hasil dekripsi:",
            bg=self.bg_color,
            font=("Segoe UI", 10),
            fg=self.dark_color
        ).pack(anchor=tk.W)
        
        output_frame = tk.Frame(output_section, bg=self.bg_color)
        output_frame.pack(fill=tk.X, pady=8)
        
        output_entry = tk.Entry(
            output_frame,
            textvariable=self.output_file_path,
            width=65,
            state='readonly',
            font=("Consolas", 10),
            relief=tk.SOLID,
            bd=1
        )
        output_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        
        tk.Button(
            output_frame,
            text="💾 Save As...",
            command=self.select_output_file,
            bg=self.accent_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=5
        ).pack(side=tk.LEFT)
        
        # ========== ACTION SECTION ==========
        action_section = tk.Frame(self.decrypt_frame, bg=self.bg_color)
        action_section.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(
            action_section,
            text="🔓 Extract and Decrypt",
            command=self.extract_and_decrypt,
            bg=self.success_color,
            fg="white",
            font=("Segoe UI", 14, "bold"),
            height=2,
            cursor="hand2",
            relief=tk.FLAT
        ).pack(fill=tk.X)
    
    # ========== EVENT HANDLERS ==========
    
    def select_plaintext_file(self):
        """Select file to encrypt"""
        filename = filedialog.askopenfilename(
            title="Select Secret File",
            initialdir="test_files",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.plaintext_file_path.set(filename)
            self.update_status(f"File dipilih: {Path(filename).name}")
    
    def select_cover_image(self):
        """Select cover image and display preview"""
        filename = filedialog.askopenfilename(
            title="Select Cover Image",
            initialdir="test_images",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg *.jpeg")
            ]
        )
        if filename:
            self.cover_image_path.set(filename)
            self.display_image_preview(filename, self.cover_preview_label)
            self.update_status(f"Cover image dipilih: {Path(filename).name}")
    
    def select_stego_image(self):
        """Select stego image and display preview"""
        filename = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[
                ("PNG Files", "*.png"),
                ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )
        if filename:
            self.stego_image_path.set(filename)
            self.display_image_preview(filename, self.stego_preview_label)
            self.update_status(f"Stego image dipilih: {Path(filename).name}")
    
    def select_output_file(self):
        """Select output file location"""
        filename = filedialog.asksaveasfilename(
            title="Save Decrypted File As",
            initialdir="test_files",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.output_file_path.set(filename)
            self.update_status(f"Output akan disimpan sebagai: {Path(filename).name}")
    
    def display_image_preview(self, image_path, label_widget):
        """Display image preview in label"""
        try:
            img = Image.open(image_path)
            
            # Get image info
            width, height = img.size
            img_info = f"{width}x{height} px"
            
            # Resize for preview
            img.thumbnail((450, 250))
            photo = ImageTk.PhotoImage(img)
            
            label_widget.configure(image=photo, text="")
            label_widget.image = photo  # Keep reference
            
            # Show image info below preview
            info_text = f"\n{Path(image_path).name}\nSize: {img_info}"
            # Create compound label with image and text
            
        except Exception as e:
            label_widget.configure(
                text=f"Error loading image:\n{str(e)}",
                image="",
                fg="red"
            )
    
    def encrypt_and_hide(self):
        """Perform encryption and hiding operation"""
        # Validation
        if not self.plaintext_file_path.get():
            messagebox.showwarning("Warning", "Silakan pilih file yang ingin dienkripsi!")
            return
        
        if not self.cover_image_path.get():
            messagebox.showwarning("Warning", "Silakan pilih cover image!")
            return
        
        # Get output path
        output_path = filedialog.asksaveasfilename(
            title="Save Stego Image As",
            defaultextension=".png",
            initialfile="secret_stego_image.png",
            filetypes=[("PNG Files", "*.png")]
        )
        
        if not output_path:
            return
        
        # Force PNG extension (CRITICAL!)
        if not output_path.lower().endswith('.png'):
            output_path = output_path.rsplit('.', 1)[0] + '.png'
            messagebox.showinfo("Info", "Output file akan disimpan sebagai PNG (required untuk LSB)")
        
        # Perform encryption
        self.update_status("🔄 Encrypting and hiding data... Please wait...")
        self.root.update()
        
        try:
            success, message = self.crypto_system.encrypt_and_hide(
                plaintext_file_path=self.plaintext_file_path.get(),
                cover_image_path=self.cover_image_path.get(),
                output_image_path=output_path
            )
            
            if success:
                messagebox.showinfo("Success! ✓", 
                                  f"{message}\n\n"
                                  f"Stego image dapat dibuka sebagai gambar biasa.\n"
                                  f"Data rahasia tersembunyi di dalamnya.")
                self.update_status("✓ Encryption completed successfully!")
            else:
                messagebox.showerror("Error", f"✗ {message}")
                self.update_status("✗ Encryption failed!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{str(e)}")
            self.update_status("✗ Error occurred!")
    
    def extract_and_decrypt(self):
        """Perform extraction and decryption operation"""
        # Validation
        if not self.stego_image_path.get():
            messagebox.showwarning("Warning", "Silakan pilih stego image!")
            return
        
        if not self.output_file_path.get():
            messagebox.showwarning("Warning", "Silakan tentukan lokasi output file!")
            return
        
        # Perform decryption
        self.update_status("🔄 Extracting and decrypting data... Please wait...")
        self.root.update()
        
        try:
            success, message = self.crypto_system.extract_and_decrypt(
                stego_image_path=self.stego_image_path.get(),
                output_file_path=self.output_file_path.get()
            )
            
            if success:
                messagebox.showinfo("Success! ✓", f"{message}")
                self.update_status("✓ Decryption completed successfully!")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Open File?", 
                                     "Dekripsi berhasil!\n\nApakah ingin membuka file sekarang?"):
                    try:
                        os.startfile(self.output_file_path.get())
                    except:
                        # For non-Windows systems
                        import subprocess
                        subprocess.call(['open', self.output_file_path.get()])
            else:
                messagebox.showerror("Error", f"✗ {message}")
                self.update_status("✗ Decryption failed!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{str(e)}")
            self.update_status("✗ Error occurred!")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CryptoStegoGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()