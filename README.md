# 🔎 Semantic Product Search Engine

A semantic product search engine that uses **sentence embeddings** and **ChromaDB** to find products based on the meaning of a user's search query rather than relying only on exact keyword matching.

## 📌 Overview

Traditional product search often depends on matching the exact words entered by a user with words contained in product descriptions.

This project takes a different approach.

Product categories and descriptions are converted into numerical representations called **embeddings** using the `BAAI/bge-small-en-v1.5` Sentence Transformer model. These embeddings are stored in **ChromaDB**, a vector database that allows the application to retrieve products that are semantically similar to a user's query.

For example, a user can search for:

> `waterproof backpack`

and the application retrieves products whose descriptions are semantically closest to the query.

The application provides an interactive search interface using **Gradio**.

---

## ✨ Key Features

- 🔎 Semantic product search using embeddings
- 🧠 Sentence Transformer model for text embeddings
- 🗄️ Persistent ChromaDB vector database
- 📐 Cosine-based similarity search
- 📊 Similarity scores for retrieved products
- 🖥️ Interactive Gradio web interface
- 🐳 Docker support
- ⚡ Embeddings are generated only when the ChromaDB collection is empty

---

## 🧠 How It Works

The application follows this pipeline:

```text
Online Shopping Dataset
          │
          ▼
   Data Preprocessing
          │
          ▼
Product Category + Description
          │
          ▼
 Sentence Transformer
 (BAAI/bge-small-en-v1.5)
          │
          ▼
    Embeddings
          │
          ▼
      ChromaDB
          │
          │
          │       User Search Query
          │              │
          │              ▼
          │       Query Embedding
          │              │
          └──────────────┤
                         ▼
                  Similarity Search
                         │
                         ▼
                Matching Products
                         │
                         ▼
                 Similarity Score
```

### Search Process

1. The product dataset is loaded using Pandas.
2. Duplicate product records are removed.
3. Product category and product description are combined into searchable text.
4. The Sentence Transformer model converts the product text into embeddings.
5. The embeddings are stored persistently in ChromaDB.
6. When a user enters a search query, the query is converted into an embedding.
7. ChromaDB retrieves the closest matching products using cosine distance.
8. The application converts the returned distance into a similarity score.
9. Results are displayed through the Gradio interface.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Pandas | Dataset loading and preprocessing |
| NumPy | Numerical operations and similarity score calculation |
| Sentence Transformers | Generating text embeddings |
| BAAI/bge-small-en-v1.5 | Embedding model |
| ChromaDB | Vector database and similarity search |
| Gradio | Interactive web interface |
| python-dotenv | Environment configuration |
| Docker | Application containerization |

---

## 📊 Dataset

This project uses the **Online Shopping Dataset** by **Jackson Divakar R**, sourced from Kaggle.

The dataset contains online shopping transaction and product information.

For the semantic search component, the project primarily uses:

- `Product_SKU`
- `Product_Category`
- `Product_Description`

The product category and description are combined to create the text used for embedding generation.

During experimentation, the dataset contained approximately **52,955 records**, while preprocessing reduced the product search collection to approximately **1,153 unique product records**.

> Dataset attribution: Jackson Divakar R — Online Shopping Dataset — Kaggle.

---

## 🗂️ Project Structure

```text
Project3/
│
├── first.py
├── prod.csv
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
├── README.md
│
└── test.ipynb
```

### Generated / Local Files

The following files and folders are intentionally excluded from version control:

```text
chroma_db/
.gradio/
.env
__pycache__/
```

`chroma_db/` contains the locally generated vector database and embeddings. It is recreated by the application when the collection is empty.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Project3
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Run:

```bash
python first.py
```

The application will start the Gradio interface.

Open the local URL shown in the terminal, typically:

```text
http://127.0.0.1:7860
```

or:

```text
http://localhost:7860
```

### First Run

On the first run:

1. The dataset is loaded.
2. Product information is prepared.
3. Embeddings are generated.
4. Embeddings are stored in ChromaDB.

### Subsequent Runs

If the ChromaDB collection already contains embeddings, the application loads the existing collection instead of generating the embeddings again.

This reduces unnecessary embedding generation during subsequent application launches.

---

## 🐳 Running with Docker

The project includes a `Dockerfile` for containerized execution.

### Build the Docker image

```bash
docker build -t product-search-engine .
```

### Run the container

```bash
docker run -p 7860:7860 product-search-engine
```

Then open:

```text
http://localhost:7860
```

---

## 🔍 Example

Example query:

```text
waterproof backpack
```

The application converts the query into an embedding and searches the vector database for products with similar semantic meaning.

The interface returns the closest matching products along with their similarity scores.

---

## 💾 Why ChromaDB?

Instead of calculating similarity between a new query and every product manually, the project uses ChromaDB as a vector database.

ChromaDB stores the product embeddings and allows the application to efficiently retrieve the closest vectors to a query embedding.

The database is persisted locally in:

```text
chroma_db/
```

The generated database is intentionally excluded from Git because it can be recreated from the source dataset and application code.

---

## 🧠 Embeddings

An embedding is a numerical representation of text that captures aspects of its meaning.

For this project:

```text
Product Category + Product Description
                    ↓
          Sentence Transformer
                    ↓
              Embedding Vector
                    ↓
                 ChromaDB
```

The same process is applied to a user's search query.

The application then compares the query embedding with the stored product embeddings to retrieve semantically similar products.

---

## 📸 Screenshots

Screenshots of the running application can be added here.

Example:

```markdown
![Product Search Engine](screenshots/product-search.png)
```

---

## 🔮 Future Improvements

Potential improvements include:

- Add product images to search results
- Include product price and additional product information
- Add filtering by product category
- Add price-range filtering
- Improve ranking and relevance evaluation
- Add hybrid keyword + semantic search
- Add a larger and more diverse product dataset
- Deploy the application as a public web service
- Add automated evaluation of search relevance
- Add search history and analytics

---

## 📚 Learning Outcomes

This project helped me gain practical experience with:

- Text embeddings
- Semantic search
- Vector databases
- Sentence Transformer models
- Similarity search
- Data preprocessing
- Persistent vector storage
- Gradio interfaces
- Docker containerization
- Building an end-to-end AI-powered application

---

## 📄 Dataset Attribution

**Dataset:** Online Shopping Dataset  
**Author:** Jackson Divakar R  
**Source:** Kaggle

The dataset is used as the product catalog for demonstrating semantic product search.

---

## 👨‍💻 Author

**Anvesh Prasade**

This project was developed as a practical implementation of semantic search using embeddings and vector databases.