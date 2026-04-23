# 🎬 Movie Recommendation System

A content-based movie recommendation system built with Python and Machine Learning that suggests similar movies based on genres, keywords, and plot overview.

## 🌍 Live Demo
[Click here to try the app!](https://movie-recommendation-system-lknhvdju4agg3wnzzpastt.streamlit.app/)

## 🧠 How It Works
1. Combines movie genres, keywords, overview into single tags
2. Converts text to vectors using CountVectorizer
3. Calculates cosine similarity between 4800+ movies
4. Returns top 5 most similar movies with posters and ratings
5. Fuzzy search for typos and TMDB fallback for unknown movies

## ✨ Features
- 🔍 Smart search with fuzzy matching
- 🎯 ML-powered content-based recommendations
- 🖼️ Real movie posters via TMDB API
- ⭐ Movie ratings
- 🌐 Unknown movie fallback using genre matching

## 🛠️ Tech Stack
- **Python** - Core programming
- **Pandas & NLTK** - Data processing
- **Scikit-learn** - ML vectorization & similarity
- **Streamlit** - Web application
- **TMDB API** - Movie posters & ratings

## 🚀 Run Locally
1. Clone the repo
```bash
   git clone https://github.com/varchasva02/movie-recommendation-system.git
```
2. Install requirements
```bash
   pip install -r requirements.txt
```
3. Add your TMDB API key in `config.py`
```python
   TMDB_API_KEY = "your_key_here"
```
4. Run the app
```bash
   streamlit run app.py
```

## 📊 Dataset
TMDB 5000 Movies Dataset from Kaggle

## 🤝 Connect
Made by [varchasva02](https://github.com/varchasva02)
