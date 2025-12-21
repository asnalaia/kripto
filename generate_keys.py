"""
Generate RSA Key Pair
Jalankan file ini SEKALI untuk membuat private_key.pem dan public_key.pem

Run: python generate_keys.py
"""

from Crypto.PublicKey import RSA

def generate_keypair():
    """Generate RSA keypair (2048 bit)"""
    print("[*] Generating RSA keypair (2048 bit)...")
    
    # Generate private key
    private_key = RSA.generate(2048)
    
    # Generate public key from private key
    public_key = private_key.publickey()
    
    # Save private key
    with open("private_key.pem", "wb") as f:
        f.write(private_key.export_key())
    print("[+] Private key saved: private_key.pem")
    
    # Save public key
    with open("public_key.pem", "wb") as f:
        f.write(public_key.export_key())
    print("[+] Public key saved: public_key.pem")
    
    print("\n✅ RSA keypair generated successfully!")
    print("⚠️  Keep private_key.pem SECRET!")
    print("📤 You can share public_key.pem")

if __name__ == "__main__":
    generate_keypair()