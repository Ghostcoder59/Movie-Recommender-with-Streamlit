import pickle
import streamlit as st
import requests
import random

# Function to fetch poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/150"

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


# Streamlit App
st.set_page_config(page_title="Movie Recommender", layout="wide", initial_sidebar_state="expanded")

# Add a banner image
st.image("https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/f562aaf4-5dbb-4603-a32b-6ef6c2230136/dh0w8qv-9d8ee6b2-b41a-4681-ab9b-8a227560dc75.jpg/v1/fill/w_1280,h_720,q_75,strp/the_netflix_login_background__canada__2024___by_logofeveryt_dh0w8qv-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NzIwIiwicGF0aCI6IlwvZlwvZjU2MmFhZjQtNWRiYi00NjAzLWEzMmItNmVmNmMyMjMwMTM2XC9kaDB3OHF2LTlkOGVlNmIyLWI0MWEtNDY4MS1hYjliLThhMjI3NTYwZGM3NS5qcGciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.LOYKSxIDqfPwWHR0SSJ-ugGQ6bECF0yO6Cmc0F26CQs", use_column_width=True)

st.title("Movie Recommender System")
st.markdown("""
Welcome to the **Movie Recommender System**!  
Select a movie from the dropdown or search for it to get personalized recommendations.
""")

# Load data
movies = pickle.load(open('/Users/ravindergalley/Desktop/Movie_Recommender/movie_list.pkl', 'rb'))
similarity = pickle.load(open('/Users/ravindergalley/Desktop/Movie_Recommender/similarity.pkl', 'rb'))

movie_list = movies['title'].values

# Sidebar for user input
st.sidebar.title("Search and Recommend")
selected_movie = st.sidebar.selectbox("Type or select a movie:", movie_list)

# Show recommendations button
if st.sidebar.button('Show Recommendations'):
    with st.spinner("Fetching recommendations..."):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.markdown("### Recommended Movies")
    cols = st.columns(5)  # Display recommendations in 5 columns
    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[idx], caption=recommended_movie_names[idx], use_column_width=True)

    # Add ratings and genres (placeholder values for now)
    st.markdown("### Details for Recommended Movies")
    for idx, name in enumerate(recommended_movie_names):
        with st.expander(f"Details for {name}"):
            st.write(f"**Genre:** Action/Adventure | **Rating:** 8.{idx+1}/10")
            st.write("**Description:** A thrilling story of...")

# Random Movie Button
if st.sidebar.button("Random Movie"):
    random_movie = random.choice(movie_list)
    st.sidebar.markdown(f"🎥 How about trying **{random_movie}**?")

# Footer
st.markdown("---")
st.markdown("💡 **Pro Tip**: Use the search bar in the sidebar for quick access to movies!")
