import base64
import subprocess
import sys
from pathlib import Path

song_file = Path(sys.argv[1])

# 1) Read song bytes
binary_data = song_file.read_bytes()

# 2) Encode to base64 text
encoded_song = base64.b64encode(binary_data).decode()

# 3) Modify placeholder to force commit
with open("placeholder.txt", "a") as f:
    f.write("🎵\n")

# 4) Stage changes
subprocess.run(["git", "add", "placeholder.txt"])

# 5) Commit with encoded song in commit message
subprocess.run(["git", "commit", "-m", f"SONG_DATA:{encoded_song}"])

print("✅ Song hidden in commit history successfully!")

