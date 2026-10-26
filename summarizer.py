from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from chunker import chunk_transcript
import re
from nltk.tokenize import sent_tokenize

MODEL_NAME = "philschmid/bart-large-cnn-samsum"

print("Loading BART model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def summarize_text(text, max_len=150, min_len=40):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=1024,
    )
    summary_ids = model.generate(
        **inputs,
        max_length=max_len,
        min_length=min_len,
        num_beams=4,
        no_repeat_ngram_size=3,
        length_penalty=2.0,
        early_stopping=True,
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize_transcript(transcript):
        # Remove short closing/pleasantry sentences ("Thank you very much.", "Applause")
    pleasantry = re.compile(r"\b(thank you|thanks|applause)\b", re.IGNORECASE)
    sentences = [
        s for s in sent_tokenize(transcript)
        if not (pleasantry.search(s) and len(s.split()) < 12)
    ]
    transcript = " ".join(sentences)
    transcript = " ".join(transcript.split())
    # Map step: summarize each chunk separately
    chunks = chunk_transcript(transcript, max_words=600)
    print(f"Summarizing {len(chunks)} chunk(s)...")

    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{len(chunks)}")
        summaries.append(summarize_text(chunk))

    # Only one chunk? That summary is the final one
    if len(summaries) == 1:
        return summaries[0]

    combined = " ".join(summaries)

    # Skip the reduce step if the combined text is already short;
    # re-summarizing short text makes the model invent content
    if len(combined.split()) < 250:
        return combined

    # Reduce step: summarize the combined chunk summaries
    print("Combining chunk summaries into final summary...")
    return summarize_text(combined, max_len=200, min_len=60)

if __name__ == "__main__":
    with open("audio/transcript.txt", "r", encoding="utf-8") as f:
        transcript = f.read()

    final_summary = summarize_transcript(transcript)

    print("\n--- FINAL SUMMARY ---\n")
    print(final_summary)

    with open("audio/summary.txt", "w", encoding="utf-8") as f:
        f.write(final_summary)
    print("\nSaved to audio/summary.txt")