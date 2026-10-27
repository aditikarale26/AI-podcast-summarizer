import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

from nltk.tokenize import sent_tokenize

def chunk_transcript(transcript, max_words=800):
    sentences = sent_tokenize(transcript)

    # Split any oversized "sentence" (e.g. missing punctuation) into word-based pieces
    pieces = []
    for s in sentences:
        words = s.split()
        if len(words) > max_words:
            for i in range(0, len(words), max_words):
                pieces.append(" ".join(words[i:i + max_words]))
        else:
            pieces.append(s)

    chunks = []
    current_chunk = []
    current_word_count = 0

    for piece in pieces:
        word_count = len(piece.split())
        if current_word_count + word_count > max_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0
        current_chunk.append(piece)
        current_word_count += word_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

if __name__ == "__main__":
    with open("audio/transcript.txt", "r", encoding="utf-8") as f:
        transcript = f.read()

    chunks = chunk_transcript(transcript)

    print(f"Transcript split into {len(chunks)} chunk(s)")
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ({len(chunk.split())} words) ---")
        print(chunk[:200] + "...")