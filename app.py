import pickle
import streamlit as st
import pandas as pd
import requests


api_key = "ad26761976d9d5350a28f9c8215cd871"
url = "https://api.themoviedb.org/3"
poster_url = "https://image.tmdb.org/t/p/w500/"

class Recommend:
    def __init__(self,api_key):
        self.api_key = api_key
        self.url = url


    def search_movie(self,movie):
        search_url = f"{url}/movie/movie"
        response = requests.get(search_url,params={'api_key':api_key, 'language': 'en-US','query':movie})
        response.raise_for_status()
        search_result = response.json()['results']

        if search_result:
            result = search_result[0]
            title = result['title']
            id = result['id']
            popularity = result['popularity']
            realse_date = result['release_date']
            lang = result['original_language']
            overview = result['overview']
            return title,id,popularity,realse_date,lang,overview
        else:
            None, None


    
    def recommend(self,movie):
        movie_index = movies[movies['title'] == movie].index
        if not movie_index.empty:  # Check if movie is found
            distance = similarity[movie_index[0]]
            movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

            recommend_movie = []
            for i in movie_list:
                recommend_movie.append(movies.iloc[i[0]].to_dict())  # Return dictionary for each movie
            return recommend_movie
        else:
            return []  # Return empty list if no recommendations

    def fetch_poster(self,movie_id):
        response = requests.get(f"{url}/movie/{movie_id}?api_key={api_key}")
        data = response.json()

        if 'poster_path' in data:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else :
            "URL_to_a_default_image_or_placeholder"


def display_movie_details(recommendation):
    st.markdown(
             f"""
                 <div class="card">
                     <div class="card-body">
                         <img " class="card-img-top" alt="" onclick="flipCard(this)">
                         <div class="card-content" style="display: none;">
                             <h4>{recommendation['title']}</h4>
                             <p>Popularity: {recommendation.get('popularity', 0)}</p>
                             <p>Release Date: {recommendation.get('release_date',0)}</p>
                             <p>Language: {recommendation.get('language',0)}</p>
                             <p>{recommendation.get('overview',0)}</p>
                         </div>
                     </div>
                 </div>
     """,
         unsafe_allow_html=True
        )
recommend = Recommend(api_key)


# load pickle file
similarity = pickle.load(open('similarity.pkl','rb'))
movie_dict = pickle.load(open('movies.pkl','rb'))

movies = pd.DataFrame(movie_dict)

st.title("Movie Recommend System !")
select_movie = st.selectbox('what movie you want to recommend',movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend.recommend(select_movie)
    
    # for j in recommendations:
    #     st.write(j)
    if not recommendations:
        st.error('No Movie Found Try Again !')
    
    else :
        st.header('Recommended Movies ')
        

        num_cols = 5  # Set the number of columns

        # Create columns dynamically based on recommendations
        cols = st.columns(min(len(recommendations), num_cols))

        for i, recommendation in enumerate(recommendations):
            if isinstance(recommendation, dict):
                col = cols[i % num_cols]  # Use modulo to distribute recommendations across columns
                col.write(recommendation['title'])
                poster_url = recommend.fetch_poster(recommendation['id'])
                col.markdown(
            f"""
            <div class="card">
                <div class="card-body">
                    <img src="{poster_url}" class="card-img-top" alt="{recommendation['title']}" onclick="flipCard(this)">
                    <div class="card-content" style="display: none;">
                        {display_movie_details(recommendation)}  </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        else:
            st.warning("No recommendation found at this position.")