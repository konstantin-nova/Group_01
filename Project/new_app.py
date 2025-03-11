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
N = st.sidebar.number_input("Select N for Top Movie Genres", min_value=1, max_value=10, value=5, key="genre_n")

# Plot 1: Movie Genre Distribution
st.subheader("Movie Genre Distribution")
try:
    # Get the top N movie genres from the analyzer
    genre_counts = analyzer.movie_type(N)

    # Create a plot
    fig1, ax1 = plt.subplots()
    ax1.bar(genre_counts['movie_type'], genre_counts['count'], color='skyblue')

    # Set labels and title
    ax1.set_ylabel("Count")
    ax1.set_xlabel("Movie Genre")
    ax1.set_title("Top Movie Genres")

    # Rotate x-axis labels for better readability
    ax1.set_xticklabels(genre_counts['movie_type'], rotation=45, ha='right')

    # Display plot in Streamlit
    st.pyplot(fig1)
except Exception as e:
    st.error(f"Error processing movie genre data: {e}")

# Plot 2: Actor Count Per Movie
st.subheader("Actor Count Per Movie")
try:
    # Use the actor_count method instead of direct data access
    actor_histogram = analyzer.actor_count()
    
    # Calculate reasonable x-axis limits based on data
    max_actors = actor_histogram['number_of_actors'].max()
    x_limit = min(max_actors, 50)  # Limit to 50 actors max for better visibility
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.histplot(data=actor_histogram[actor_histogram['number_of_actors'] <= x_limit], 
                x='number_of_actors', 
                weights='movie_count',
                bins=25,
                kde=True, 
                ax=ax2, 
                color='lightcoral')
    
    ax2.set_xlabel("Number of Actors per Movie")
    ax2.set_ylabel("Number of Movies")
    ax2.set_title("Actor Count Distribution (up to 50 actors)")
    
    # Format y-axis to use K for thousands
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}K' if x >= 1000 else str(int(x))))
    
    # Add grid for better readability
    ax2.grid(True, alpha=0.3)
    
    st.pyplot(fig2)
except Exception as e:
    st.error(f"Error processing actor count data: {e}")

# Plot 3: Actor Height Distribution
st.subheader("Actor Height Distribution")
try:
    gender = st.selectbox("Select Gender", ["All", "M", "F"])
    min_height = st.number_input("Min Height (meters)", min_value=1.0, max_value=2.5, value=1.5)
    max_height = st.number_input("Max Height (meters)", min_value=1.0, max_value=2.5, value=2.0)

    # Use the actor_distributions method instead of direct data filtering
    height_counts = analyzer.actor_distributions(gender=gender, max_height=max_height, min_height=min_height)

    fig3, ax3 = plt.subplots()
    sns.histplot(data=height_counts, x='height', weights='count', bins=20, kde=True, ax=ax3, color='seagreen')
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