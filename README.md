# MOVIE SEARCH AND RECOMMENDATION SYSYTEM:

# Movie Recommendation System

A content-based movie recommendation system built with Python, Pandas, and Scikit-learn. The interactive web interface is powered by Streamlit, allowing users to get movie suggestions in real-time.

## 🎥 Demo
🎥 [Watch the demo video here](https://vimeo.com/1127148989)

*(This is a sample screen recording. You can create your own and replace the link!)*

---


## ✨ Features

* **Content-Based Filtering:** Recommends movies by analyzing features like overview, genre, cast, and director.
* **Interactive UI:** Search for any movie in the dataset and get instant recommendations through a user-friendly Streamlit web app.
* **Real-time Data:** Uses the TMDB API to fetch up-to-date movie posters and details.

---

## ⚙️ How It Works

The recommendation logic is based on **content-based filtering**.

1.  **Data Preprocessing:** The `movies.csv` and `credits.csv` datasets are merged and cleaned. Key features (genres, keywords, cast, crew) are extracted and combined into a single text block called "tags" for each movie.
2.  **Text Vectorization:** The "tags" for all movies are converted into numerical vectors using `CountVectorizer`. This process creates a high-dimensional vector space where each movie is represented by a point. 
3.  **Similarity Calculation:** The **cosine similarity** is calculated between all movie vectors. Cosine similarity measures the angle between two vectors, with a smaller angle indicating higher similarity.
4.  **Recommendation:** When a user selects a movie, the system finds its vector and returns the top movies with the highest cosine similarity scores.

---

## 🛠️ Local Setup and Installation

Follow these steps to set up and run the project on your local machine.

**1. Clone the Repository:**
```bash
git clone [https://github.com/piyush-sm-08/movie_search_and_recommendation_system.git)](https://github.com/YOUR_USERNAME/movie_recommender.git)
cd movie_recommender
```
*(Replace `YOUR_USERNAME` with your actual GitHub username.)*

**2. Download the Dataset:**
This project uses the "TMDB 5000 Movie Dataset" from Kaggle.
* Download it from [https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_credits.csv , https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
* Unzip the file and place `movies.csv` and `credits.csv` inside a `data/` folder in the project directory.

**3. Create and Activate a Virtual Environment:**
* **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* **On Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

**4. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**5. Generate the Model Files:**
The recommendation model is pre-computed using a Jupyter Notebook.
* Open and run all the cells in the `recommend.ipynb` notebook.
* This will process the data and create two essential files: `movie_list.pkl` and `similarity.pkl` inside a `trove/` folder.

---

## 🚀 Usage

Once the setup is complete, you can run the Streamlit web application.

```bash
streamlit run app.py
```

Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`). Search for a movie and enjoy the recommendations!