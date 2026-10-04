from faster_whisper import WhisperModel

def transcribe_audio(audio_path):
    model = WhisperModel("small", device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_path)

    print(f"Detected language: {info.language}")

    transcript = ""
    for segment in segments:
        transcript += segment.text + " "

    return transcript.strip()

if __name__ == "__main__":
    text = transcribe_audio("audio/podcast.wav")
    print("\n--- TRANSCRIPT ---\n")
    print(text)

    with open("audio/transcript.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("\nSaved to audio/transcript.txt")