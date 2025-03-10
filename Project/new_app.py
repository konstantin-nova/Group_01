import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from movie_data_analysis import MovieDataAnalyzer  # Import your MovieDataAnalyzer class

# Initialize the movie analysis module
analyzer = MovieDataAnalyzer()

# Streamlit App Title
st.title("Movie Analysis Dashboard")

# Sidebar: Settings
st.sidebar.header("Settings")
N = st.sidebar.number_input("Select N for Top Movie Genres", min_value=1, max_value=10, value=5)

# Plot 1: Movie Genre Distribution
st.subheader("Movie Genre Distribution")
try:
    # Extract and count genres
    genre_counts = (
        analyzer.movie_metadata["movie_genres"]
        .dropna()
        .str.split(",")  # Split multiple genres
        .explode()  # Flatten the list
        .value_counts()
        .head(N)  # Get top N genres
    )

    fig1, ax1 = plt.subplots()
    genre_counts.plot(kind='bar', color='skyblue', ax=ax1)
    ax1.set_ylabel("Count")
    ax1.set_xlabel("Movie Genre")
    ax1.set_title("Top Movie Genres")
    st.pyplot(fig1)
except Exception as e:
    st.error(f"Error processing movie genre data: {e}")

# Plot 2: Actor Count Per Movie
st.subheader("Actor Count Per Movie")
try:
    actor_counts = analyzer.characters["wikipedia_movie_id"].value_counts()

    fig2, ax2 = plt.subplots()
    sns.histplot(actor_counts, bins=20, kde=True, ax=ax2, color='lightcoral')
    ax2.set_xlabel("Number of Actors per Movie")
    ax2.set_ylabel("Frequency")
    ax2.set_title("Actor Count Distribution")
    st.pyplot(fig2)
except Exception as e:
    st.error(f"Error processing actor count data: {e}")

# Plot 3: Actor Height Distribution
st.subheader("Actor Height Distribution")
try:
    gender = st.selectbox("Select Gender", ["All", "M", "F"])
    min_height = st.number_input("Min Height (meters)", min_value=1.0, max_value=2.5, value=1.5)
    max_height = st.number_input("Max Height (meters)", min_value=1.0, max_value=2.5, value=2.0)

    filtered_df = analyzer.characters.dropna(subset=["actor_height"])
    if gender != "All":
        filtered_df = filtered_df[filtered_df["actor_gender"] == gender]

    filtered_df = filtered_df[
        (filtered_df["actor_height"] >= min_height) & (filtered_df["actor_height"] <= max_height)
    ]

    fig3, ax3 = plt.subplots()
    sns.histplot(filtered_df["actor_height"], bins=20, kde=True, ax=ax3, color='seagreen')
    ax3.set_xlabel("Height (meters)")
    ax3.set_ylabel("Frequency")
    ax3.set_title(f"Height Distribution for {gender}")
    st.pyplot(fig3)
except Exception as e:
    st.error(f"Error processing actor height data: {e}")

# Data Previews
st.subheader("Data Previews")
st.write("Movie Metadata:")
st.dataframe(analyzer.movie_metadata.head())

st.write("Character Metadata:")
st.dataframe(analyzer.characters.head())

# Notes
st.info("This app is built using the `MovieDataAnalyzer` class, loading and visualizing movie and character data.")