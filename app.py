import pickle
import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_TOKEN")


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "Authorization": f"Bearer {TMDB_TOKEN}",
        "accept": "application/json"
    }

    params = {
        "language": "en-US"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    except requests.exceptions.RequestException as e:
        print("TMDB Error:", e)

    return None

def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_posters.append(
            fetch_poster(movie_id)
        )

        recommended_movie_names.append(
            movies.iloc[i[0]].title
        )

    return recommended_movie_names, recommended_movie_posters


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies_path = os.path.join(BASE_DIR, "movies_dict.pkl")
similarity_path = os.path.join(BASE_DIR, "similarity.pkl")


# Load movies dictionary
with open(movies_path, "rb") as file:
    movies_dict = pickle.load(file)

# Convert dictionary to DataFrame
movies = pd.DataFrame(movies_dict)


# Load similarity matrix
with open(similarity_path, "rb") as file:
    similarity = pickle.load(file)


st.header("Movie Recommender System")


movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):

    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        if recommended_movie_posters[0]:
            st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        if recommended_movie_posters[1]:
            st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        if recommended_movie_posters[2]:
            st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        if recommended_movie_posters[3]:
            st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        if recommended_movie_posters[4]:
            st.image(recommended_movie_posters[4])