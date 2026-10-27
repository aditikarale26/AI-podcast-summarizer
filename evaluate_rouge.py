from itertools import islice
from datasets import load_dataset
from rouge_score import rouge_scorer
from summarizer import summarize_text

NUM_SAMPLES = 30   # test with 10 first, then change to 30

# Stream the test split so you don't download the whole dataset
dataset = load_dataset(
    "abisee/cnn_dailymail", "3.0.0", split="test", streaming=True
)

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
totals = {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}

for i, sample in enumerate(islice(dataset, NUM_SAMPLES)):
    generated = summarize_text(sample["article"], max_len=130, min_len=40)
    scores = scorer.score(sample["highlights"], generated)

    for key in totals:
        totals[key] += scores[key].fmeasure

    print(f"Sample {i+1}/{NUM_SAMPLES} done")

print("\n--- AVERAGE ROUGE SCORES ---")
results = []
for key, value in totals.items():
    line = f"{key}: {value / NUM_SAMPLES:.4f}"
    print(line)
    results.append(line)

with open("rouge_results.txt", "w") as f:
    f.write(f"Samples: {NUM_SAMPLES}\n" + "\n".join(results))
print("\nSaved to rouge_results.txt")