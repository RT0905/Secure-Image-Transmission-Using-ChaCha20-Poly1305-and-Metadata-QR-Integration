import cv2
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os
from PIL import Image
import qrcode
import hashlib
import matplotlib.pyplot as plt
from datetime import datetime


def encrypt_images():
    num_images = int(input("🔢 How many images do you want to encrypt? "))

    for i in range(num_images):
        print(f"\n🖼️ Processing Image {i + 1}/{num_images}")

        # === STEP 1: Load & preprocess image ===
        filename = input("Enter image filename (with extension): ").strip()
        image = cv2.imread(filename)

        if image is None:
            print(f"❌ Image '{filename}' not found. Skipping.")
            continue

        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        image = cv2.resize(image, (512, 512))

        # === STEP 2: Add pattern overlay ===
        pattern = np.tile([[255, 0], [0, 255]], (256, 256))
        pattern_colored = np.stack([pattern] * 3, axis=-1).astype(np.uint8)
        image_padded = cv2.addWeighted(image, 0.95, pattern_colored, 0.05, 0)

        # === STEP 3: Encrypt image ===
        image_bytes = image_padded.tobytes()
        key = ChaCha20Poly1305.generate_key()
        nonce = os.urandom(12)
        chacha = ChaCha20Poly1305(key)
        ciphertext = chacha.encrypt(nonce, image_bytes, None)

        encrypted_filename = f"encrypted_image_{i + 1}.bin"
        with open(encrypted_filename, "wb") as f:
            f.write(nonce + ciphertext)

        key_filename = f"secret_key_{i + 1}.key"
        with open(key_filename, "wb") as f:
            f.write(key)

        # === STEP 4: Generate QR code ===
        hash_id = hashlib.sha256(ciphertext[:256]).hexdigest()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sender = "Riva Tikoo"
        qr_data = f"ImageID:{hash_id}\nSender:{sender}\nTime:{timestamp}"

        qr = qrcode.make(qr_data)
        qr_filename = f"image_qr_{i + 1}.png"
        qr.save(qr_filename)

        # === STEP 5: Display QR Code ===
        qr_img = Image.open(qr_filename)
        plt.figure(figsize=(4, 4))
        plt.imshow(qr_img)
        plt.title(f"✅ QR Code for Image {i + 1}")
        plt.axis("off")
        plt.show()

        print(f"✅ Done! Files for Image {i + 1}:\n- {encrypted_filename}\n- {qr_filename}\n- {key_filename}")


def decrypt_images():
    num_files = int(input("How many encrypted images do you want to decrypt? "))

    for i in range(num_files):
        print(f"\n🔓 Decrypting Image {i + 1}/{num_files}")

        encrypted_filename = input("Enter encrypted .bin filename: ").strip()
        key_filename = input("Enter corresponding .key filename: ").strip()

        try:
            with open(encrypted_filename, "rb") as f:
                encrypted = f.read()

            with open(key_filename, "rb") as f:
                key = f.read()

            nonce = encrypted[:12]
            ciphertext = encrypted[12:]

            chacha = ChaCha20Poly1305(key)
            decrypted_bytes = chacha.decrypt(nonce, ciphertext, None)

            decrypted_image = np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape((512, 512, 3))
            output_filename = f"decrypted_image_{i + 1}.png"
            cv2.imwrite(output_filename, decrypted_image)

            plt.imshow(cv2.cvtColor(decrypted_image, cv2.COLOR_BGR2RGB))
            plt.title(f"🖼️ Decrypted Image {i + 1}")
            plt.axis("off")
            plt.show()

            print(f"✅ Decrypted and saved as '{output_filename}'.")

        except FileNotFoundError as e:
            print(f"❌ File not found: {e}")
        except Exception as e:
            print(f"❌ Error while decrypting Image {i + 1}: {e}")


if __name__ == "__main__":
    print("1. Encrypt Images")
    print("2. Decrypt Images")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        encrypt_images()
    elif choice == "2":
        decrypt_images()
    else:
        print("❌ Invalid choice. Exiting.")