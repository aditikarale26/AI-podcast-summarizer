# AI Podcast Summarizer

An NLP pipeline that takes a YouTube video/podcast URL and generates a short summary of its spoken content. Built as a project for the NLP subject.

## Pipeline

```
YouTube URL
   -> yt-dlp          downloads and extracts audio (.wav)
   -> Whisper         speech-to-text transcription
   -> NLTK            sentence splitting + chunking
   -> BART            summarizes each chunk (map step)
   -> BART            summarizes combined chunk summaries (reduce step, long videos only)
   -> Final summary
```

## Tools used

| Stage | Tool |
|---|---|
| Audio extraction | yt-dlp (+ FFmpeg) |
| Transcription | faster-whisper (OpenAI Whisper, `small` model) |
| Sentence splitting | NLTK |
| Summarization | BART (`philschmid/bart-large-cnn-samsum`) via HuggingFace transformers |

All models are pretrained and run locally. No API keys are needed.

## Files

| File | Purpose |
|---|---|
| `download.py` | YouTube URL -> `audio/podcast.wav` |
| `transcribe.py` | audio -> `audio/transcript.txt` |
| `chunker.py` | transcript -> sentence-safe chunks |
| `summarizer.py` | chunks -> final summary (`audio/summary.txt`) |

## Setup

Python 3.11 is recommended (some libraries don't support newer versions yet).

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

FFmpeg is also required:

```bash
winget install "FFmpeg (Essentials Build)"
```

## Usage

```bash
python main.py          # paste a YouTube URL, get the summary
python evaluate_rouge.py   # ROUGE evaluation on 30 CNN/DailyMail samples
```

## Model comparison

| Model | Observation |
|---|---|
| `facebook/bart-large-cnn` (news-trained) | Copied spoken-language stutters and added content not in the video |
| `philschmid/bart-large-cnn-samsum` (dialogue-trained) | Much cleaner and more faithful summaries on spoken transcripts |

## Status

- [x] Audio download
- [x] Transcription
- [x] Chunking
- [x] Map-reduce summarization
- [x] ROUGE evaluation on CNN/DailyMail
- [x] Single-command pipeline (`main.py`)

## Results

ROUGE scores on 30 CNN/DailyMail test samples (summarization module only):

| Metric | Score |
|---|---|
| ROUGE-1 | 0.3540 |
| ROUGE-2 | 0.1560 |
| ROUGE-L | 0.2511 |

## Known limitations

- Whisper `small` can misspell proper nouns (e.g. "Alvin" transcribed as "elven"), and the summary inherits those errors.
- Abstractive summarization can occasionally invent or distort details that aren't in the transcript.
- Transcription runs on CPU and is slow for long videos (about 11 minutes for a 17-minute talk).