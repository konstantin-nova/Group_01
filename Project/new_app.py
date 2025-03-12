"""
new_app.py

This Streamlit application provides a dashboard for movie data analysis using 
the `MovieDataAnalyzer` class. It includes visualizations for movie genre 
distribution, actor count per movie, actor height distribution, movie releases 
over time, and actor birthdate distribution.

Modules:
    streamlit: For creating the web application.
    matplotlib.pyplot: For creating plots.
    seaborn: For creating statistical visualizations.
    movie_data_analysis: Contains the `MovieDataAnalyzer` class for analyzing 
    movie data.

Usage:
    Run the script to start the Streamlit application. Navigate through the 
    sidebar to access different pages and visualizations.

Pages:
    Main Page: Displays visualizations for movie genre distribution, actor 
    count per movie, and actor height distribution.
    Movie Release Info: Displays visualizations for movie releases over time 
    and actor birthdate distribution.

Note:
    This app is built using the `MovieDataAnalyzer` class, loading and 
    visualizing movie and character data.
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
# Import your MovieDataAnalyzer class
from movie_data_analysis import MovieDataAnalyzer

# Initialize the movie analysis module
analyzer = MovieDataAnalyzer()

# Navigation to pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main Page", "Movie Release Info"])

if page == "Main Page":
    # Streamlit App Title
    st.title("Movie Analysis Dashboard")

    # Sidebar: Input
    st.sidebar.header("Input Parameters")
    n = st.sidebar.number_input(
        "Select n for Top Movie Genres", min_value=1, max_value=10, value=5, key="genre_n")

    # Plot 1: Movie Genre Distribution
    st.subheader("Movie Genre Distribution")
    try:
        # Get the top n movie genres from the analyzer
        genre_counts = analyzer.movie_type(n)

        # Create a plot
        fig1, ax1 = plt.subplots()
        ax1.bar(genre_counts['movie_type'],
                genre_counts['count'], color='skyblue')

        # Set labels and title
        ax1.set_ylabel("Count")
        ax1.set_xlabel("Movie Genre")
        ax1.set_title("Top Movie Genres")

        # Rotate x-axis labels for better readability
        ax1.set_xticklabels(
            genre_counts['movie_type'], rotation=45, ha='right')

        # Display plot in Streamlit
        st.pyplot(fig1)
    except (KeyError, ValueError) as e:
        st.error(f"Error processing movie genre data: {e}")

    # Plot 2: Actor Count Per Movie
    st.subheader("Actor Count Per Movie")
    try:
        # Use the actor_count method instead of direct data access
        actor_histogram = analyzer.actor_count()

        # Calculate reasonable x-axis limits based on data
        max_actors = actor_histogram['number_of_actors'].max()
        # Limit to 50 actors max for better visibility
        x_limit = min(max_actors, 50)

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
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'{int(x/1000)}K' if x >= 1000 else str(int(x))))

        # Add grid for better readability
        ax2.grid(True, alpha=0.3)

        st.pyplot(fig2)
    except (KeyError, ValueError) as e:
        st.error(f"Error processing actor count data: {e}")

    # Plot 3: Actor Height Distribution
    st.subheader("Actor Height Distribution")
    try:
        gender = st.selectbox("Select Gender", ["All", "M", "F"])
        min_height = st.number_input(
            "Min Height (meters)", min_value=1.0, max_value=2.5, value=1.5)
        max_height = st.number_input(
            "Max Height (meters)", min_value=1.0, max_value=2.5, value=2.0)

        # Use the actor_distributions method
        height_counts = analyzer.actor_distributions(
            gender=gender, max_height=max_height, min_height=min_height)

        fig3, ax3 = plt.subplots()
        sns.histplot(data=height_counts, x='height', weights='count',
                     bins=20, kde=True, ax=ax3, color='seagreen')
        ax3.set_xlabel("Height (meters)")
        ax3.set_ylabel("Frequency")
        ax3.set_title(f"Height Distribution for {gender}")
        st.pyplot(fig3)
    except (KeyError, ValueError) as e:
        st.error(f"Error processing actor height data: {e}")

    # Data Previews
    st.subheader("Data Previews")
    st.write("Movie Metadata:")
    st.dataframe(analyzer.movie_metadata.head())

    st.write("Character Metadata:")
    st.dataframe(analyzer.characters.head())


if page == "Movie Release Info":
    st.title("Movie Release Information")

    # Display Movie Releases Over Time
    st.subheader("Movie Releases Over Time")

    # Input for genre selection
    selected_genre = st.text_input("Enter Genre")

    try:
        # Get chronological data for the selected genre
        data = analyzer.releases(selected_genre)

        # Create a bar plot
        fig4, ax4 = plt.subplots()
        ax4.bar(data['year'], data['count'], color='dodgerblue')

        # Set labels and title
        ax4.set_ylabel("Count")
        ax4.set_xlabel("Year")
        ax4.set_title(f"Number of {selected_genre} Movies Over Time")

        # Display plot in Streamlit
        st.pyplot(fig4)
    except (KeyError, ValueError) as e:
        st.error(f"Error processing chronological data: {e}")

    # Display Actor birthdate distribution
    st.subheader("Actor Birthdate Distribution")

    try:
        # Input for time period selection from dropdown
        selected_period = st.selectbox("Select Time Period", ["Year", "Month"])

        # Map Year to Y and Month to M
        period_map = {"Year": "Y", "Month": "M"}
        selected_period = period_map[selected_period]

        # Get birthdate data
        birthdate_data = analyzer.ages(selected_period)
        # Dynamically change the number of bins based on the period
        bins = birthdate_data['period'].nunique()

        # Create a plot
        fig5, ax5 = plt.subplots()
        ax5.bar(birthdate_data['period'],
                birthdate_data['count'], color='salmon')

        # Set labels and title
        if selected_period == "Y":
            ax5.set_xlabel("Birth Year")
            ax5.set_title("Actor Birth Year Distribution")
        else:
            ax5.set_xlabel("Birth Month")
            ax5.set_title("Actor Birth Month Distribution")
            ax5.set_ylim(0)
            ax5.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax5.set_ylabel("Frequency")

        # Rotate x-axis labels for better readability
        ax5.set_xticklabels(birthdate_data['period'], rotation=45, ha='right')

        # Display plot in Streamlit
        st.pyplot(fig5)

        # Add note that actors whose birthmonth is unknown are counted shown in January
        st.info(
            "Note: Actors whose birth month is unknown are receive January as default.")
    except (KeyError, ValueError) as e:
        st.error(f"Error processing birthdate data: {e}")

# Notes
st.info("This app is built using the `MovieDataAnalyzer` class, "
        "loading and visualizing movie and character data.")
