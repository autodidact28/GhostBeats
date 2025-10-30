import hashlib

def sha256sum(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

orig_hash = sha256sum("song.mp3")
decoded_hash = sha256sum("decoded_song.mp3")

print("Original SHA256:", orig_hash)
print("Decoded  SHA256:", decoded_hash)

if orig_hash == decoded_hash:
    print("✅ Integrity Verified — Both files are identical!")
else:
    print("❌ Files differ — something went wrong during commit/merge.")

