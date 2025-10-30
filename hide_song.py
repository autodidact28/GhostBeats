import base64
import subprocess
import sys
from pathlib import Path

song_file = Path(sys.argv[1])

# 1) Read bytes from file
binary_data = song_file.read_bytes()

# 2) Base64 encode (convert to safe text)
encoded_song = base64.b64encode(binary_data).decode()

# 3) Split into chunks
chunk_size = 5000
chunks = [encoded_song[i:i+chunk_size] for i in range(0, len(encoded_song), chunk_size)]

print(f"Total chunks: {len(chunks)}")

# 4) Store each chunk in its own commit
for i, chunk in enumerate(chunks):
    # Make dummy change so commit has something to track
    with open("placeholder.txt", "a") as f:
        f.write(f"part {i}\n")
    
    subprocess.run(["git", "add", "placeholder.txt"])
    subprocess.run(["git", "commit", "-m", f"SONG_CHUNK:{chunk}"])

print("✅ Full song stored across commit history in multiple chunks.")

