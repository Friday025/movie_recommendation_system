import pickle
import pandas as pd
import streamlit as st


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index
    distances = similarity[movie_index[0]]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    for i in movie_list:
        movie_id = i[0]
        # featch poster from API
        recommend_movies.append(movies.iloc[i[0]].title)

    return recommend_movies


similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_dict = pickle.load(open('movies.pkl', 'rb'))

movies = pd.DataFrame(movie_dict)

st.title('Movie Recommender system')

select_movie = st.selectbox("what movie you like best ", movies['title'].values)

if st.button("Recommend"):
    recommendation = recommend(select_movie)
    for j in recommendation:
        st.write(j)
