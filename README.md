# Secure Image Transmission Using ChaCha20-Poly1305 and Metadata QR Integration

## 🔐 Overview

This project implements a secure image transmission system using the **ChaCha20-Poly1305** authenticated encryption algorithm. It ensures the **confidentiality**, **integrity**, and **authenticity** of image data. For added security and convenience, crucial decryption metadata is encoded into a **QR code**, allowing safe out-of-band transmission.

---

## 🛠️ Features

- 📷 Encrypts image files using **ChaCha20-Poly1305 (AEAD)**
- 🔐 Ensures confidentiality, integrity, and authenticity
- 🔄 Generates unique nonce and authentication tag for each encryption
- 🧾 Embeds metadata into a QR code:
  - Encryption Key *(for demo purposes only — avoid in production)*
  - Nonce
  - Authentication Tag
  - Image hash or timestamp
- 📤 Supports secure transmission of encrypted image and QR code separately
- 🔓 Decrypts the image using metadata from the QR code

---

## 📦 Dependencies

Install required Python packages using pip:

```
pip install cryptography opencv-python qrcode Pillow numpy
```

---

## 📂 Project Structure

```
Secure-Image-Transmission-Using-ChaCha20-Poly1305-and-Metadata-QR-Integration/
│
├── encrypt_image.py       # Encrypts image and generates metadata QR
├── decrypt_image.py       # Decrypts image using QR metadata
├── utils.py               # Helper functions for encryption, QR handling, etc.
├── sample_image.jpg       # Example input image
├── encrypted_image.bin    # Output encrypted image (binary format)
├── metadata_qr.png        # QR code containing encryption metadata
└── README.md              # Project documentation
```

---

## 🧪 Usage

### 🔒 Encrypt an Image

```
python encrypt_image.py --input sample_image.jpg --output encrypted_image.bin --qr metadata_qr.png
```

- Encrypts the input image
- Saves encrypted binary and QR code with metadata

### 🔓 Decrypt an Image

```
python decrypt_image.py --input encrypted_image.bin --qr metadata_qr.png --output decrypted_image.jpg
```

- Parses QR code
- Extracts metadata
- Decrypts image and reconstructs the original file

---

## ✅ Security Considerations

- 🚫 **Never include the encryption key inside the QR code in production!**
- ✅ This demo includes the key for simplicity and educational purposes
- 🔐 In a secure system:
  - Use a secure key exchange method (e.g., Diffie-Hellman)
  - Transmit key separately or derive from a shared secret
  - Use additional transport security (e.g., HTTPS or VPN)

---

## 📸 Example Workflow

1. Encrypt the image:
    - `sample_image.jpg` → `encrypted_image.bin` + `metadata_qr.png`
2. Send the `encrypted_image.bin` via a public or insecure channel
3. Send the `metadata_qr.png` via a secure or offline channel
4. Recipient scans the QR code, decrypts the image using the metadata

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**[Your Name]**  
Made with ❤️ and crypto.
