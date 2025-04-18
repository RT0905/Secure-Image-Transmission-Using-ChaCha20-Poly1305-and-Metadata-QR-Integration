# === SENDER SIDE SCRIPT ===
import cv2
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os
from PIL import Image
import qrcode
import hashlib
import matplotlib.pyplot as plt
from datetime import datetime

# === STEP 1: Load & preprocess image ===
image = cv2.imread("elon_musk.png")

if image is None:
    raise ValueError("❌ Image not found. Please upload 'elon_musk.png'.")

# Fix channel issues
if len(image.shape) == 2:
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
elif image.shape[2] == 4:
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

# Resize to standard shape
image = cv2.resize(image, (512, 512))

# === STEP 2: Add pattern overlay (light distortion) ===
pattern = np.tile([[255, 0], [0, 255]], (256, 256))
pattern_colored = np.stack([pattern]*3, axis=-1).astype(np.uint8)
image_padded = cv2.addWeighted(image, 0.95, pattern_colored, 0.05, 0)

# === STEP 3: Encrypt image ===
image_bytes = image_padded.tobytes()

key = ChaCha20Poly1305.generate_key()
nonce = os.urandom(12)
chacha = ChaCha20Poly1305(key)
ciphertext = chacha.encrypt(nonce, image_bytes, None)

# Save encrypted file (nonce + ciphertext)
with open("encrypted_image.bin", "wb") as f:
    f.write(nonce + ciphertext)

# Save key separately for receiver
with open("secret_key.key", "wb") as f:
    f.write(key)

# === STEP 4: Generate QR code with metadata (not the key) ===
hash_id = hashlib.sha256(ciphertext[:256]).hexdigest()
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sender = "Riva Tikoo"
qr_data = f"ImageID:{hash_id}\nSender:{sender}\nTime:{timestamp}"

qr = qrcode.make(qr_data)
qr.save("image_qr.png")

# === STEP 5: Display QR code after everything is sent ===
qr_img = Image.open("image_qr.png")
plt.figure(figsize=(4, 4))
plt.imshow(qr_img)
plt.title("✅ Image QR Code (Sent)")
plt.axis("off")
plt.show()

print("✅ Sender process complete.\nFiles generated:\n- encrypted_image.bin\n- image_qr.png\n- secret_key.key")



# === RECEIVER SIDE ===
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import cv2
import matplotlib.pyplot as plt

# === LOAD ENCRYPTED FILE AND KEY ===
with open("encrypted_image.bin", "rb") as f:
    encrypted = f.read()

with open("secret_key.key", "rb") as f:
    key = f.read()

nonce = encrypted[:12]
ciphertext = encrypted[12:]

# === DECRYPT IMAGE ===
chacha = ChaCha20Poly1305(key)
decrypted_bytes = chacha.decrypt(nonce, ciphertext, None)
decrypted_image = np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape((512, 512, 3))
cv2.imwrite("decrypted_by_receiver.png", decrypted_image)

# === DISPLAY IMAGE ===
plt.imshow(cv2.cvtColor(decrypted_image, cv2.COLOR_BGR2RGB))
plt.title("Decrypted Image")
plt.axis("off")
plt.show()


