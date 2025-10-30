import base64
import subprocess

# Step 1: Get all commit messages in chronological order
log_output = subprocess.check_output(
    ["git", "log", "--reverse", "--pretty=%B"],
    text=True
)

# Step 2: Extract all lines starting with "SONG_CHUNK:"
chunks = []
for line in log_output.splitlines():
    if line.startswith("SONG_CHUNK:"):
        chunks.append(line.replace("SONG_CHUNK:", "").strip())

# Step 3: Combine all Base64 chunks
full_base64 = "".join(chunks)

# Step 4: Decode and write to output file
decoded_data = base64.b64decode(full_base64)
with open("decoded_song.mp3", "wb") as f:
    f.write(decoded_data)

print(f"✅ Reconstructed song saved as decoded_song.mp3")
print(f"Total chunks combined: {len(chunks)}")

