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

import re
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack_integrations.components.generators.ollama import OllamaGenerator
from movie_data_analysis import (
    MovieDataAnalyzer,
    MovieTypeRequest,
    ActorFilter,
    GenreFilter
)


# Initialize the movie analysis module
analyzer = MovieDataAnalyzer()

# Navigation to pages
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", ["Main Page", "Chronological Info", "Classification"])

if page == "Main Page":
    # Streamlit App Title
    st.title("Movie Analysis Dashboard")

    # Plot 1: Movie Genre Distribution
    st.subheader("Movie Genre Distribution")
    try:
        n = st.number_input("Select number of Genres",
                            min_value=1, max_value=50, value=5,
                            key="genre_n")

        movie_type_request = MovieTypeRequest(n=n)
        # Get the top n movie genres from the analyzer
        genre_counts = analyzer.movie_type(movie_type_request)

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
        sns.histplot(
            data=actor_histogram[
                actor_histogram['number_of_actors'] <= x_limit],
            x='number_of_actors', weights='movie_count', bins=25, kde=True,
            ax=ax2, color='lightcoral')

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

        actor_filter = ActorFilter(gender=gender,
                                   max_height=max_height,
                                   min_height=min_height)
        # Use the actor_distributions method
        height_counts = analyzer.actor_distributions(actor_filter)

        fig3, ax3 = plt.subplots()
        sns.histplot(data=height_counts, x='height', weights='count',
                     bins=20, kde=True, ax=ax3, color='seagreen')
        ax3.set_xlabel("Height (meters)")
        ax3.set_ylabel("Frequency")
        ax3.set_title(f"Height Distribution for {gender}")
        st.pyplot(fig3)
    except (KeyError, ValueError) as e:
        st.error(f"Error processing actor height data: {e}")

if page == "Chronological Info":
    st.title("Chronological Information about the Movies")

    # Display Movie Releases Over Time
    st.subheader("Movie Releases Over Time")

    # Input for genre selection
    selected_genre = st.text_input("Enter Genre")

    try:
        genre_filter = GenreFilter(genre=selected_genre)
        # Get chronological data for the selected genre
        data = analyzer.releases(genre_filter=genre_filter)

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
            ax5.set_xlim(
                birthdate_data['period'].min(), birthdate_data['period'].max())
        else:
            ax5.set_xlabel("Birth Month")
            ax5.set_title("Actor Birth Month Distribution")
            ax5.set_ylim(0)
            ax5.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

            # Rotate x-axis labels for better readability
            ax5.set_xticklabels(
                birthdate_data['period'], rotation=45, ha='right')

        ax5.set_ylabel("Frequency")

        # Display plot in Streamlit
        st.pyplot(fig5)

        # Add note Actors with unknown birth months are shown in January
        if selected_period == "M":
            st.info(
                "Note: Actors with unknown birth "
                "months are shown in January by default.")

    except (KeyError, ValueError) as e:
        st.error(f"Error processing birthdate data: {e}")

if page == "Classification":
    st.title("Classification of Movies")

    # Display Movie Classification
    st.subheader("AI Movie Classification")

    # Button to shuffle and get a random movie
    if st.button("Shuffle"):
        try:
            # Get a random movie title and summary
            random_movie = analyzer.movie_metadata.sample(1)
            movie_title = random_movie['movie_name'].values[0]

            # Get the wikipedia movie id
            movie_id = random_movie['wikipedia_movie_id'].values[0]

            # Get the plot summary
            movie_summary = analyzer.plot_summaries.loc[
                analyzer.plot_summaries[
                    'wikipedia_movie_id'] == movie_id, 'summary']

            if not movie_summary.empty:
                MOVIE_SUMMARY = movie_summary.values[0]
            else:
                MOVIE_SUMMARY = "Summary not available."

            # Extract the genres from the movie data
            movie_genres = random_movie['movie_genres'].str.extractall(
                r'\"([^\"]+)\"')[0].unique()

            # Remove genre ids
            movie_genres = [
                genre for genre in movie_genres if not genre.startswith('/m/')]

            # Display the movie title
            st.text_area("Movie Title and Summary",
                         movie_title + "\n\n" + MOVIE_SUMMARY)

            # Display the genres from the database
            st.text_area("Genres in Database:", ", ".join(movie_genres))

            # Use a local LLM to classify the movie summary

            # Prepare the prompt for the LLM
            PROMPT = """
            Given only the following information, answer the question.
            Classify the genres of the movie based on the title and the
            summary.
            You can classify multiple genres.\n
            ONLY print the names of Genres, separated by commas.\n
            Do not include any other information in the response.\n\n
            Example output: Action, Adventure, Comedy\n
            Title: {{movie_title}}
            Summary: {{movie_summary}}
            """

            # Initialize pipeline
            pipe = Pipeline()
            pipe.add_component("prompt_builder", PromptBuilder(
                template=PROMPT,
                required_variables=["movie_title", "movie_summary"]))
            pipe.add_component("llm", OllamaGenerator(
                model="deepseek-r1:1.5B"))

            # Connect the components
            pipe.connect("prompt_builder", "llm")

            # Run the pipeline
            response = pipe.run({"prompt_builder": {
                "movie_title": movie_title,
                "movie_summary": movie_summary
            }
            })

            # Extract the classified genres
            classified_genres = response["llm"]["replies"][0]

            # Display the classified genres
            if "<think>" in classified_genres:
                classified_genres = re.sub(
                    r"<think>.*?</think>\s*", "",
                    classified_genres, flags=re.DOTALL)

            # Display the classified genres
            st.text_area("Classified Genres by LLM", classified_genres)

            # Create follow-up question
            # Follow up prompt
            FOLLOWUP_PROMPT = """
            Given only the following information, answer the question.
            Does one of the classified genres match at least one of the actual
            genres of the movie?
            Your classification: {{classified_genres}}\n
            Actual genres: {{actual_genres}}\n

            ONLY write the one of the following responses.
            Your response should not contain any other information.\n\n

            If at least one classifed genre EXACTLY matches a genre in the
            actual genres, write:\n
            'I correctly classified one or more genres'.\n\n

            If none of the classified genres matches the actual genres,
            write:\n
            'I did not correctly classify any genres'.
            """

            # Initialize the follow-up pipeline
            pipe_followup = Pipeline()
            pipe_followup.add_component(
                "followup_prompt_builder",
                PromptBuilder(template=FOLLOWUP_PROMPT,
                              required_variables=[
                                  "classified_genres",
                                  "actual_genres"
                                  ]))
            pipe_followup.add_component(
                "llm", OllamaGenerator(model="deepseek-r1:1.5B"))
            pipe_followup.connect("followup_prompt_builder", "llm")

            # Run the follow-up pipeline
            followup_response = pipe_followup.run({
                "followup_prompt_builder": {
                    "classified_genres": classified_genres,
                    "actual_genres": movie_genres
                }
            })

            # Extract the response
            evaluation = followup_response["llm"]["replies"][0]

            # If response contains <think> tags, clean up the respons
            if "<think>" in evaluation:
                evaluation = re.sub(r"<think>.*?</think>\s*",
                                    "", evaluation, flags=re.DOTALL)

            # Display the evaluation
            st.text_area("Evaluation", evaluation)
        except (KeyError, ValueError, RuntimeError) as e:
            st.error(f"Error classifying movie: {e}")
