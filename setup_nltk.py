import os
import nltk

nltk_data_path = os.path.expanduser('~/nltk_data')
os.makedirs(os.path.join(nltk_data_path, "tokenizers", "punkt"), exist_ok=True)
nltk.download("punkt", download_dir=nltk_data_path)

print(f"✅ NLTK punkt installed to: {nltk_data_path}")
