# import pickle
# import streamlit as st
# import requests

# # TMDB API configuration
# TMDB_V4_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YzU3ODdkNzI5MTU1NDk2NDk3ZmZiMTRkZTQzOWU3OCIsIm5iZiI6MTc1NTU5MTQ5Ny4wNTksInN1YiI6IjY4YTQzMzQ5YmI0NTI4MTk2ODU2N2UwYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rzU8LBK-fWbJANYswj3-J30xqd-rVvnA0OlDHjotVas"

# def fetch_movie_details(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {TMDB_V4_TOKEN}"
#     }
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()  # Ensures it fails gracefully if network fails
#     return response.json()


# def fetch_poster(movie_id):
#     """
#     Return poster URL using TMDB API.
#     """
#     data = fetch_movie_details(movie_id)
#     if data and data.get("poster_path"):
#         return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
#     return "https://via.placeholder.com/500x750?text=No+Image"


# def recommend(movie):
#     movies_index=movies[movies['title']==movie].index[0]
#     distance=similarity[movies_index]
#     movie_list=sorted(list(enumerate(similarity[movies_index])),reverse=True,key=lambda x:x[1])[1:8]
#     recommended_movies_name=[]
#     recommended_movies_poster=[]

#     for i in movie_list:
#         movie_id=movies.iloc[i[0]]['movie_id']
#         recommended_movies_poster.append(fetch_poster(movie_id))
#         recommended_movies_name.append(movies.iloc[i[0]]['title'])
#     return recommended_movies_name,recommended_movies_poster

# st.header("🎬 Movie Recommendation System")
# movies=pickle.load(open('trove/movie_list.pkl','rb'))
# similarity = pickle.load(open('trove/similarity.pkl','rb'))

# movies_list= movies['title'].values

# selected_movie=st.selectbox('Search movies,series,anime',movies_list)

# if st.button('Show movies'):
#     recommended_movies_name , recommended_movies_poster = recommend(selected_movie)
#     col1,col2,col3,col4,col5,col6,col7=st.columns(7)

import joblib
import streamlit as st
import requests
import time
from requests.adapters import HTTPAdapter, Retry

# ---------------------------------------------
# 🔑 TMDB API Configuration
# ---------------------------------------------
TMDB_V4_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YzU3ODdkNzI5MTU1NDk2NDk3ZmZiMTRkZTQzOWU3OCIsIm5iZiI6MTc1NTU5MTQ5Ny4wNTksInN1YiI6IjY4YTQzMzQ5YmI0NTI4MTk2ODU2N2UwYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rzU8LBK-fWbJANYswj3-J30xqd-rVvnA0OlDHjotVas"

# ---------------------------------------------
# ⚙️ Setup a requests session with retry logic
# ---------------------------------------------
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# ---------------------------------------------
# 🎬 Fetch Movie Details
# ---------------------------------------------
@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    """Fetch movie details from TMDB."""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_V4_TOKEN}"
        }
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"⚠️ Error fetching movie {movie_id}: {e}")
        return {}

# ---------------------------------------------
# 🖼️ Poster URL helper
# ---------------------------------------------
def get_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

# ---------------------------------------------
# 🎞️ Recommendation Logic
# ---------------------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:8]

    recommended_names = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        data = fetch_movie_details(movie_id)
        recommended_names.append(data.get("title", "Unknown"))
        recommended_posters.append(get_poster_url(data.get("poster_path")))
        time.sleep(0.3)  # avoid API rate limit
    return recommended_names, recommended_posters

# ---------------------------------------------
# 🧠 Load Data (using joblib)
# ---------------------------------------------
try:
    movies = joblib.load('src/trove/movie_list.pkl')
    similarity = joblib.load('src/trove/similarity.pkl')
except FileNotFoundError:
    st.error("❌ Required model files not found in 'src/trove/'.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Error loading model files: {e}")
    st.stop()

# ---------------------------------------------
# 🌐 Streamlit UI
# ---------------------------------------------
st.set_page_config(page_title="🎬 Movie Recommendation System", layout="wide")

st.title("🎬 Movie Search and Recommendation System")
selected_movie = st.selectbox("Search for a movie:", movies['title'].values)

if st.button("SUBMIT: 🎥"):
    with st.spinner("Fetching movie info..."):
        # --- Show selected movie on top ---
        selected_movie_id = movies[movies['title'] == selected_movie].iloc[0].movie_id
        movie_info = fetch_movie_details(selected_movie_id)

        st.subheader(f"🎯 {movie_info.get('title', 'Unknown Movie')}")
        colA, colB = st.columns([1, 2])
        with colA:
            st.image(get_poster_url(movie_info.get("poster_path")), use_container_width=True)
        with colB:
            st.markdown(f"**Rating:** ⭐ {movie_info.get('vote_average', 'N/A')}/10")
            st.markdown(f"**Release Date:** {movie_info.get('release_date', 'N/A')}")
            st.markdown(f"**Overview:** {movie_info.get('overview', 'No description available.')}")

        st.markdown("---")

        # --- Show recommendations below ---
        st.subheader("📽️ You might also like:")
        names, posters = recommend(selected_movie)
        cols = st.columns(7)
        for idx, col in enumerate(cols):
            if idx < len(names):
                with col:
                    st.text(names[idx])
                    st.image(posters[idx])


# import pickle
# import streamlit as st
# import requests
# import time
# from requests.adapters import HTTPAdapter, Retry

# # ---------------------------------------------
# # 🔑 TMDB API Configuration
# # ---------------------------------------------
# TMDB_V4_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YzU3ODdkNzI5MTU1NDk2NDk3ZmZiMTRkZTQzOWU3OCIsIm5iZiI6MTc1NTU5MTQ5Ny4wNTksInN1YiI6IjY4YTQzMzQ5YmI0NTI4MTk2ODU2N2UwYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rzU8LBK-fWbJANYswj3-J30xqd-rVvnA0OlDHjotVas"

# # ---------------------------------------------
# # ⚙️ Setup a requests session with retry logic
# # ---------------------------------------------
# session = requests.Session()
# retries = Retry(
#     total=5,                # retry up to 5 times
#     backoff_factor=1,       # wait 1s, 2s, 4s, ...
#     status_forcelist=[429, 500, 502, 503, 504],  # handle API/server errors
# )
# adapter = HTTPAdapter(max_retries=retries)
# session.mount("http://", adapter)
# session.mount("https://", adapter)

# # ---------------------------------------------
# # 🎬 Fetch Movie Details from TMDB
# # ---------------------------------------------
# def fetch_movie_details(movie_id):
#     """
#     Fetch full movie details (title, overview, poster, etc.) using TMDB API.
#     Returns the JSON response or {} on error.
#     """
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
#         headers = {
#             "accept": "application/json",
#             "Authorization": f"Bearer {TMDB_V4_TOKEN}"
#         }
#         response = session.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         print(f"⚠️ Error fetching movie {movie_id}: {e}")
#         return {}

# # ---------------------------------------------
# # 🖼️ Fetch Poster URL (Cached)
# # ---------------------------------------------
# @st.cache_data(show_spinner=False)
# def fetch_poster(movie_id):
#     """
#     Return poster URL using TMDB API, with caching to avoid redundant requests.
#     """
#     data = fetch_movie_details(movie_id)
#     if data and data.get("poster_path"):
#         return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
#     return "https://via.placeholder.com/500x750?text=No+Image"

# # ---------------------------------------------
# # 🎞️ Recommendation Logic
# # ---------------------------------------------
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movie_list = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )[0:8]

#     recommended_names = []
#     recommended_posters = []
#     for i in movie_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_names.append(movies.iloc[i[0]].title)
#         recommended_posters.append(fetch_poster(movie_id))
#         time.sleep(0.3)  # prevent API rate-limit
#     return recommended_names, recommended_posters

# # ---------------------------------------------
# # 🧠 Load Saved Data
# # ---------------------------------------------
# try:
#     movies = pickle.load(open('trove/movie_list.pkl', 'rb'))
#     similarity = pickle.load(open('trove/similarity.pkl', 'rb'))
# except FileNotFoundError:
#     st.error("❌ Required model files not found in 'trove/'.")
#     st.stop()

# # ---------------------------------------------
# # 🌐 Streamlit UI
# # ---------------------------------------------
# st.set_page_config(page_title="Movie Recommender", layout="wide")
# st.title("🎬 Movie Search and Recommendation System")

# selected_movie = st.selectbox("Search or select a movie:", movies['title'].values)

# if st.button("Search 🎥"):
#     with st.spinner("Fetching movie recommendations..!"):
#         names, posters = recommend(selected_movie)

#     # Display results in grid layout
#     cols = st.columns(8)
#     for idx, col in enumerate(cols):
#         if idx < len(names):
#             with col:
#                 st.text(names[idx])
#                 st.image(posters[idx])
