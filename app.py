import streamlit as st
import pandas as pd
import pickle
import requests
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
from difflib import get_close_matches
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pickle.load(open('movies.pkl', 'rb'))
@st.cache_resource  # ← this caches it so it only runs once!
def get_similarity():
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    return cosine_similarity(vectors)

similarity = get_similarity()

def recommend_by_genre(movie_name):
    
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    data = requests.get(search_url).json()
    
    if not data['results']:
        return None, None, None
    
    genre_ids = data['results'][0]['genre_ids']
    
    genre_map = {
        28: "action", 12: "adventure",
        16: "animation", 35: "comedy",
        80: "crime", 18: "drama",
        14: "fantasy", 27: "horror",
        10749: "romance", 878: "sciencefiction",
        53: "thriller", 10752: "war"
    }
    
    genre_names = [genre_map[gid] for gid in genre_ids if gid in genre_map]
    
    if not genre_names:
        return None, None, None
    
    matched = movies[movies['tags'].str.contains(genre_names[0])]
    matched = matched.head(20)
    
    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    
    for _, row in matched.iterrows():
        recommended_movies.append(row['title'])
        poster, rating = fetch_poster(row['id'])
        recommended_posters.append(poster)
        recommended_ratings.append(rating)
    
    return recommended_movies, recommended_posters, recommended_ratings

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        data = requests.get(url).json()
        poster = "https://via.placeholder.com/500x750?text=No+Poster"
        rating = "N/A"
        if 'poster_path' in data and data['poster_path']:
            poster = "https://image.tmdb.org/t/p/w500" + data['poster_path']
        if 'vote_average' in data:
            rating = round(data['vote_average'], 1)
        return poster, rating
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster", "N/A"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    for i in movies_list[1:6]:
        mid = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster, rating = fetch_poster(mid)
        recommended_posters.append(poster)
        recommended_ratings.append(rating)
    return recommended_movies, recommended_posters, recommended_ratings

st.title("🎬 Movie Recommendation System")
search_query = st.text_input("🔍 Search for a movie:", "")

from difflib import get_close_matches

if st.button("Recommend 🎬"):
    actual_title = movies[movies['title'].str.strip().str.lower() == 
                   search_query.strip().lower()]['title'].values
    
    if len(actual_title) > 0:
        # Exact match found ✅
        names, posters, ratings = recommend(actual_title[0])
        st.subheader("Recommended Movies:")
        
    else:
        # Try fuzzy matching first!
        all_titles = movies['title'].str.lower().tolist()
        close_match = get_close_matches(search_query.lower(), 
                                       all_titles, 
                                       n=1, 
                                       cutoff=0.7)
        
        if close_match:
            # Found a close match!
            matched_title = movies[movies['title'].str.lower() == 
                           close_match[0]]['title'].values[0]
            st.info(f"🔍 Showing results for: **{matched_title}**")
            names, posters, ratings = recommend(matched_title)
            st.subheader("Recommended Movies:")
            
        else:
            # No close match - use TMDB genre search
            st.warning(f"'{search_query}' not in database! Finding similar movies...")
            names, posters, ratings = recommend_by_genre(search_query)
            st.subheader(f"Movies similar to '{search_query}':")
    
    if names:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.text(names[idx])
                st.image(posters[idx])
                st.write(f"⭐ {ratings[idx]}")
    else:
        st.error("⚠️ Could not find any recommendations!")