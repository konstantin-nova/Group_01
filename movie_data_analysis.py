"""
Movie Data Analysis Module
This module provides functionality for downloading, extracting, and
analyzing movie data.It includes a MovieDataAnalyzer class that
handles downloading data from a specified URL and extracting it for
further analysis.The module allows for efficient management of movie
datasets by:
- Checking if data has already been downloaded to avoid redundant downloads
- Creating necessary directory structures for data storage
- Downloading data from specified URLs
- Extracting compressed data files (tar.gz format)
"""

import os
import tarfile
from typing import Optional, Union
import requests
import pandas as pd
import matplotlib.pyplot as plt


class MovieDataAnalyzer:
    """Class for downloading and analyzing movie data."""
    @staticmethod
    def parse_date(date_str: Union[str, float, None]) -> pd.Timestamp:
        """
        Parses a date string into a pandas datetime object.

        This function attempts to parse a date string in various formats 
        ('%Y-%m-%d', '%Y-%m', '%Y'). If the date string is null or cannot 
        be parsed, it returns pandas NaT (Not a Time).

        Parameters:
        date_str (str): The date string to be parsed.

        Returns:
        pd.Timestamp or pd.NaT: The parsed datetime object or NaT if parsing fails.
        """
        if pd.isnull(date_str):
            return pd.NaT
        # Remove any extra spaces
        date_str = str(date_str).strip()
        # List of formats to try, ordered from most specific to least specific
        formats = ['%Y-%m-%d', '%Y-%m', '%Y']
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        return pd.NaT

    def __init__(self) -> None:
        """
        Initialize the MovieDataAnalyzer class.

        Args:
            url: URL of the data file to download
        """
        # Set the data URL
        url = 'http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz'

        # Set the download directory
        download_dir = '../downloads'

        # Create the download directory if it doesn't exist
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            print(f"Created download directory: {download_dir}")
        else:
            print(f"Download directory already exists: {download_dir}")

        # Download if file does not exist in the download directory
        tar_file_name = os.path.basename(url)  # Extract file name from URL
        tar_path = os.path.join(download_dir, tar_file_name)
        file_name = os.path.splitext(os.path.splitext(tar_file_name)[0])[0]
        dir_path = os.path.join(download_dir, file_name)
        if not os.path.exists(dir_path):
            # Download the file
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            print(f"Downloading {tar_file_name}...")

            with open(tar_path, mode='wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            print("Download complete.")

            # Extract the tarball
            print(f"Extracting {file_name}...")
            with tarfile.open(tar_path, 'r:gz') as tar:
                tar.extractall(path=download_dir, filter="data")
            print("Extraction complete.")
        else:
            print(f"File {os.path.basename(dir_path)} already exists.")

        # Instantiate dataframe attributes
        self.characters = pd.DataFrame()
        self.movie_metadata = pd.DataFrame()
        self.name_clusters = pd.DataFrame()
        self.plot_summaries = pd.DataFrame()
        self.tvtropes_clusters = pd.DataFrame()

        # Read each TSV file and create a DataFrame
        for file in os.listdir(dir_path):
            if file == "character.metadata.tsv":
                file_path = os.path.join(dir_path, file)
                ###
                # Column names from README:
                # 1. Wikipedia movie ID, 2. Freebase movie ID,
                # 3. Movie release date, 4. Character name,
                # 5. Actor date of birth, 6. Actor gender,
                # 7. Actor height (in meters),
                # 8. Actor ethnicity (Freebase ID), 9. Actor name,
                # 10. Actor age at movie release,
                # 11. Freebase character/actor map ID,
                # 12. Freebase character ID, 13. Freebase actor ID
                ###
                df = pd.read_csv(file_path, sep="\t", names=[
                    "wikipedia_movie_id", "freebase_movie_id",
                    "movie_release_date", "character_name",
                    "actor_date_of_birth", "actor_gender", "actor_height",
                    "actor_ethnicity", "actor_name",
                    "actor_age_at_movie_release",
                    "freebase_character_actor_map_id",
                    "freebase_character_id", "freebase_actor_id"
                ], encoding="utf-8", on_bad_lines="skip")
                self.characters = df  # Store as an attribute
                self.characters['actor_date_of_birth'] = \
                    self.characters['actor_date_of_birth'].apply(
                        MovieDataAnalyzer.parse_date
                )
            elif file == "movie.metadata.tsv":
                file_path = os.path.join(dir_path, file)
                ###
                # Column names from README:
                # 1. Wikipedia movie ID, 2. Freebase movie ID, 3. Movie name,
                # 4. Movie release date, 5. Movie box office revenue,
                # 6. Movie runtime,
                # 7. Movie languages (Freebase ID:name tuples),
                # 8. Movie countries (Freebase ID:name tuples),
                # 9. Movie genres (Freebase ID:name tuples)
                ###
                df = pd.read_csv(file_path, sep="\t", names=[
                    "wikipedia_movie_id", "freebase_movie_id", "movie_name",
                    "movie_release_date", "movie_box_office_revenue",
                    "movie_runtime", "movie_languages", "movie_countries",
                    "movie_genres"
                ], encoding="utf-8", on_bad_lines="skip")
                self.movie_metadata = df  # Store as an attribute
                self.movie_metadata['movie_release_date'] = \
                    self.movie_metadata['movie_release_date'].apply(
                        MovieDataAnalyzer.parse_date
                )
            elif file == "name.clusters.txt":
                file_path = os.path.join(dir_path, file)
                # Column names from README: 1. Name, 2. Actor ID
                df = pd.read_csv(file_path, sep="\t",
                                 names=["name", "actor_id"], encoding="utf-8",
                                 on_bad_lines="skip")
                self.name_clusters = df
            elif file == "plot_summaries.txt":
                ###
                # Column names from README:
                # 1. Wikipedia movie ID, 2. Plot summary
                ###
                file_path = os.path.join(dir_path, file)
                df = pd.read_csv(file_path, sep="\t",
                                 names=["wikipedia_movie_id", "summary"],
                                 encoding="utf-8", on_bad_lines="skip")
                self.plot_summaries = df  # Store as an attribute
            elif file == "tvtropes.clusters.txt":
                # Column names from README: Cluster ID and Name
                file_path = os.path.join(dir_path, file)
                df = pd.read_csv(file_path, sep="\t",
                                 names=["name", "cluster"], encoding="utf-8",
                                 on_bad_lines="skip")
                self.tvtropes_clusters = df  # Store as an attribute
            else:
                print(f"File {file} does not match any expected data file.")
        print("All files have been loaded as DataFrame attributes.")

    def movie_type(self, n: int = 10) -> pd.DataFrame:
        """
        Calculate the n most common types of movies and their counts.

        Args:
            n (int): Number of top movie types to return. Default is 10.

        Returns:
            pd.DataFrame: DataFrame with columns "Movie_Type" and "Count" for
            the top n movie types.
        """
        # Input validation
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n <= 0:
            raise ValueError("n must be a positive integer")

        # Split the movie genres into individual genres
        genres = self.movie_metadata['movie_genres'].str.split(',').explode()

        # Remove parentheses, quotes and unnecessary whitespaces from the genre names
        genres = genres.str.replace(r'["{},]', '', regex=True).str.strip()

        # Split at space to extract the genre name
        genres = genres.str.split(' ').str[-1]

        # Count the occurrences of each genre
        genre_counts = genres.value_counts().head(n).reset_index()
        genre_counts.columns = ['movie_type', 'count']

        return genre_counts

    def actor_count(self) -> pd.DataFrame:
        """
        Calculate a histogram of the number of actors vs movie counts.

        Returns:
            pd.DataFrame: DataFrame with columns "Number_of_Actors" and
            "Movie_Count".
        """
        # Group by movie ID and count the number of actors per movie
        actor_counts = self.characters.groupby('wikipedia_movie_id').size()

        # Create a histogram of the actor counts
        actor_histogram = actor_counts.value_counts().reset_index()
        actor_histogram.columns = ['number_of_actors', 'movie_count']
        actor_histogram = actor_histogram.sort_values(by='number_of_actors')

        return actor_histogram

    def actor_distributions(self, gender: str,
                            max_height: float,
                            min_height: float,
                            plot: bool = False) -> pd.DataFrame:
        """
        Calculate the distribution of actors' heights filtered by gender and
        height range.

        Args:
            gender (str): Gender to filter by ("All" or M/F).
            max_height (float): Maximum height to filter by.
            min_height (float): Minimum height to filter by.
            plot (bool): Plot the height distribution. Default is False.

        Returns:
            pd.DataFrame: DataFrame with columns "Height" and "Count" for the
            filtered actors.
        """
        if not isinstance(gender, str):
            raise TypeError("gender must be a string")
        if not isinstance(max_height, (int, float)) or \
                not isinstance(min_height, (int, float)):
            raise TypeError("max_height and min_height must be numeric")

        # Check if max_height is greater than min_height
        if max_height < min_height:
            raise ValueError("max_height must be greater than or equal to "
                             "min_height")

        # Check if height values are within a valid range
        if max_height <= 0 or min_height <= 0 or \
                max_height > 3 or min_height > 3:
            raise ValueError("max_height and min_height must be positive "
                             "values")

        # Filter the dataset by gender if specified
        if gender != "All":
            filtered_data = self.characters[
                self.characters['actor_gender'] == gender]
        else:
            filtered_data = self.characters

        # Filter the dataset by height range
        filtered_data = filtered_data[
            (filtered_data['actor_height'] <= max_height) &
            (filtered_data['actor_height'] >= min_height)
        ]

        # Drop missing values in the height column
        filtered_data = filtered_data.dropna(subset=['actor_height'])

        # Create a histogram of the heights
        height_counts = filtered_data['actor_height'].value_counts()
        height_counts = height_counts.reset_index()
        height_counts.columns = ['height', 'count']
        height_counts = height_counts.sort_values(by='height')

        # Plot the height distribution if specified
        if plot:
            # Calculate number of bins based on the range of heights
            bins = int((max_height - min_height) * 50)

            plt.figure(figsize=(10, 6))
            plt.hist(x=height_counts['height'], weights=height_counts['count'],
                     bins=bins, range=(min_height-0.05, max_height+0.05),
                     color='skyblue', density=False)
            plt.xlabel('Height (meters)')
            plt.ylabel('Count')
            plt.title(f'Height Distribution of Actors (Gender: {gender})')
            plt.show()

        return height_counts

    def releases(self, genre: Optional[str] = None) -> pd.DataFrame:
        """
        Calculate the number of movies released per year, optionally filtered by genre.

        Args:
            genre (str, optional): Genre to filter by. Default is None.

        Returns:
            pd.DataFrame: DataFrame with columns "Year" and "Count" for the 
            number of movies released per year.
        """
        # Check if genre is a string
        if genre and not isinstance(genre, str):
            raise TypeError("genre must be a string")

        # Check if genre is a valid genre
        if genre:
            valid_genres = self.movie_metadata[
                'movie_genres'].str.extractall(r'\"([^\"]+)\"')[0].unique()
            if genre not in valid_genres:
                raise ValueError("Invalid genre")

        # Create new dataframe and extract the release year from the movie release date
        releases = pd.DataFrame()
        releases['movie_release_year'] = self.movie_metadata[
            'movie_release_date'].dt.year.astype('Int64')

        # Copy the movie genres column
        releases['movie_genres'] = self.movie_metadata['movie_genres']

        # Filter by genre if specified
        if genre:
            releases = releases[releases['movie_genres'].str.contains(genre)]

        # Drop rows with missing release years
        releases = releases.dropna(subset=['movie_release_year'])

        # Count the number of movies released per year
        releases = releases['movie_release_year'].value_counts().reset_index()
        releases.columns = ['year', 'count']
        releases = releases.sort_values(by='year')

        # Sum all counts for all years
        total = releases['count'].sum()
        print(f"Total number of movies released: {total}")
        return releases

    def ages(self, period: str = 'Y') -> pd.DataFrame:
        """
        Calculate the number of births per year or month.

        Args:
            period (str): 'Y' for year, 'M' for month. Default is 'Y'.

        Returns:
            pd.DataFrame: DataFrame with columns "Period" and "Count" for the 
            number of births per year or month.
        """
        # Check if period is a correct value
        if period not in ['Y', 'M']:
            raise ValueError("period must be 'Y' for year or 'M' for month")

        # Drop rows with missing actor date of birth
        valid_births = self.characters.dropna(subset=['actor_date_of_birth'])

        if period == 'Y':
            # Extract the year from the date of birth
            valid_births['birth_year'] = valid_births['actor_date_of_birth'].dt.year
            # Remove invalid birth years
            valid_births = valid_births[valid_births['birth_year'] < 2025]
            # Count the number of births per year
            birth_counts = valid_births['birth_year'].value_counts(
            ).reset_index()
            birth_counts.columns = ['period', 'count']
            birth_counts = birth_counts.sort_values(by='period')
        else:
            # Extract the month from the date of birth
            valid_births['birth_month'] = valid_births['actor_date_of_birth'].dt.month
            # Count the number of births per month
            birth_counts = valid_births['birth_month'].value_counts(
            ).reset_index()
            birth_counts.columns = ['period', 'count']
            birth_counts = birth_counts.sort_values(by='period')
            # Map period to month names
            month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                           'July', 'August', 'September', 'October', 'November', 'December']
            birth_counts['period'] = birth_counts['period'].map(
                lambda x: month_names[x-1])

        return birth_counts
