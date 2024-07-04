import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """
    Function to clean the text by lemmatizing and removing stopwords and punctuation.
    """
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

# Load the customer support tickets dataset
df = pd.read_csv('customer_support_tickets.csv')

# Replace the placeholder {product_purchased} with the actual product names in the Ticket Description
df['Ticket Description'] = df.apply(lambda row: row['Ticket Description'].replace("{product_purchased}", row['Product Purchased']), axis=1)

# Combine Ticket Description, Ticket Type, and Ticket Subject
df['combined_text'] = df['Ticket Description'].fillna('') + ' ' + df['Ticket Type'].fillna('') + ' ' + df['Ticket Subject'].fillna('')

# Ensure no null values in the critical columns before processing
df = df.dropna(subset=['Ticket Description', 'Ticket Type', 'Ticket Subject'])

# Clean the combined text in batches
batch_size = 1000  # Adjust batch size based on your system's capability
cleaned_texts = []

for start in range(0, len(df), batch_size):
    batch_texts = df['combined_text'][start:start + batch_size]
    cleaned_batch = batch_texts.apply(clean_text)
    cleaned_texts.extend(cleaned_batch)

df['cleaned_text'] = cleaned_texts

# Train and save the vectorizer
def train_and_save_vectorizer(data, filename='vectorizer.pkl'):
    """
    Train a TF-IDF vectorizer and save it to a file.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit(data)
    joblib.dump(vectorizer, filename)
    print(f"Vectorizer saved to {filename}")

train_and_save_vectorizer(df['cleaned_text'])
