import streamlit as st
import pandas as pd
import plotly.express as px

# Read the csv
df = pd.read_csv('movie_ratings.csv')

st.set_page_config(layout="wide")

st.title("Movie Data Analysis")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    #What's the breakdown of genres for the movies that were rated?

    #Drop Duplicates
    movies_genre = df.drop_duplicates(subset=['movie_id', 'genres'])

    #Genre Count
    genre_count = movies_genre['genres'].value_counts()

    #Convert a Series to dataframe
    genre_df = genre_count.to_frame(name="count")
    genre_df = genre_df.reset_index()
    
    #Create a pie chat
    movie_breakdown = px.pie(genre_df, names='genres' ,values='count', title="🎥 Breakdown of Movies by Genre", width=600, height=600)
    
    movie_breakdown.update_traces(
        textinfo='label',
        textfont_size=14,
        hovertemplate= '%{label}<br>Count: %{value}<br>Percent: %{percent}'
    )
    
    movie_breakdown.update_layout(
    title=dict(
        font=dict(size=26
                  )
        ),
    showlegend=False
    )
    
    #Call Streamlit
    st.plotly_chart(movie_breakdown)

with col2:
    #Which genres have the highest viewer satisfaction (highest ratings)?
    st.subheader("🎬 Average Ratings by Genre") 
    
    #Which genres have the highest viewer satisfaction (highest ratings)?
    # I need genre, rating, user-id, movie-id
    # avg rating all of all genre
    genre_rating_df = pd.DataFrame({
        'Genres': df['genres'],
        'Rating': df['rating']
    })


    #Make a new df with Genre, Avg rating, Rating Count
    avg_genre_rating = genre_rating_df.groupby('Genres').agg(
        avg_rating=('Rating', 'mean'),
        rating_count=('Rating', 'count')
    ).reset_index()
    
    # Interactive, sortable table
    st.dataframe(
        avg_genre_rating,
        column_config={
        "avg_rating": st.column_config.NumberColumn(
            "Average Rating",
            format="%.2f",   # show 2 decimals
            help="Average rating of movies by genre"
        ),
        
        "rating_count": st.column_config.NumberColumn(
            "Total Rating")
        },
        
        
        width=400,
        height=500
    )
   


