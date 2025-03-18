import fitz  # PyMuPDF
from transformers import pipeline

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # BART is fast & effective

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    return text

def summarize_text(text):
    """Summarizes the extracted text efficiently."""
    if len(text) < 100:
        return "Text too short to summarize."
    
    chunk_size = 512  # Process smaller chunks for speed
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Reduce total number of chunks to process (max 5 summaries to avoid long waits)
    max_chunks = min(len(chunks), 5)  
    chunks = chunks[:max_chunks]

    # Summarize in batches (faster than one-by-one)
    summaries = summarizer(chunks, max_length=100, min_length=50, do_sample=False)

    # Combine results
    return " ".join([s["summary_text"] for s in summaries])
