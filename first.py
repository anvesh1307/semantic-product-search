import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import gradio as gr
import os
from dotenv import load_dotenv
import chromadb

load_dotenv()

# Read the port variable (defaults to 7860 if not found)
port = int(os.getenv("GRADIO_PORT", 7860))
print(f"Starting app on port: {port}")

# Startup & Data Initialization ---
#print("Loading model...")
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


client=chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="product_search",
    metadata={"hnsw:space": "cosine"}  # Set distance metric to cosine similarity
)
#Only read the CSV and Encode if the datbase is empty
if collection.count() == 0:
    print("Database empty. Loading data and generating embeddings (this only happens once)...")
    df = pd.read_csv("prod.csv")

    products = df.drop_duplicates(subset=["Product_SKU", "Product_Category", "Product_Description"]).copy()
    products["Product_Category"] = products["Product_Category"].fillna("")
    products["Product_Description"] = products["Product_Description"].fillna("")
    products["search_text"] = products["Product_Category"] + " " + products["Product_Description"]

    search_texts = products["search_text"].tolist()

    out_embds = model.encode(search_texts, show_progress_bar=True).tolist()

    ids = [str(i) for i in range(len(products))]
    metadatas = products[["Product_Category", "Product_Description"]].to_dict(orient="records")
    
    # Save everything to the local ChromaDB folder
    collection.add(
        embeddings=out_embds,
        documents=search_texts,
        metadatas=metadatas,
        ids=ids
    )
    print("Embeddings permanently saved to Chroma DB!")


else:
    print(f"Skipping generation! Loaded {collection.count()} embeddings directly from Chroma DB.")

print("Application ready!")


#Search Logic
def search_similar(query, n):
  n = int(n)  # Ensuring integer for slicing

  query_embeddings = model.encode([query]).tolist()

    # Search the vector database directly 
  results = collection.query(
    query_embeddings=query_embeddings,
    n_results=n,
    include=["metadatas", "distances"]
  )

  # Extract the metadata (categories/descriptions) and distances from the results
  metadatas = results["metadatas"][0]
  distances = results["distances"][0]

  top_results = pd.DataFrame(metadatas)
    
  # ChromaDB returns Cosine Distance. Convert Distance to a Similarity Percentage.
  top_results["Similarity Score"] = ((1 - np.array(distances)) * 100).round(2)
    
  return top_results


#Gradio Interface & Theme Configuration

my_theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="amber",
    neutral_hue="slate"
)

# 2. Added custom CSS to force the app to take up 100% of the browser width
custom_css = """
.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
}
"""
inter = gr.Interface(
    fn=search_similar,
    inputs=[
        gr.Textbox(label="Enter a Product Keyword", placeholder="Example: Waterproof Backpack"),
        gr.Slider(minimum=1, maximum=20, step=1, value=5, label="Choose Closest Matches (n)"),
    ],
    outputs=gr.Dataframe(label="Search Results"),
    title="Product Search Engine",
    description="Type in a keyword to find the closest matching products in your dataset.",
    theme=my_theme,
    css=custom_css,  # Injects the full-page width rule
    live=True        # Keeps the interactive, auto-updating functionality
)


#Containerized Launch
inter.launch(theme=my_theme)