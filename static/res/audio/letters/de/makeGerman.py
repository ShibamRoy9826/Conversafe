from pydub import AudioSegment
from pydub.silence import split_on_silence

# Load your MP3 file
audio = AudioSegment.from_file("german.mp3", format="mp3")

# Split audio where silence is at least 1000ms (1 second) long and quieter than -40 dBFS
chunks = split_on_silence(
    audio,
    min_silence_len=900,  # Minimum silence length in milliseconds
    silence_thresh=-40     # Silence threshold in decibels (relative to max volume)
)

# Export each chunk as a separate MP3 file
for i, chunk in enumerate(chunks):
    output_file = f"chunk{i+1}.mp3"
    chunk.export(output_file, format="mp3")
    print(f"Exported: {output_file}")
