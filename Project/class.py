"""
Movie Data Analysis Module
This module provides functionality for downloading, extracting, and analyzing movie data.
It includes a MovieDataAnalyzer class that handles downloading data from a specified URL
and extracting it for further analysis.
The module allows for efficient management of movie datasets by:
- Checking if data has already been downloaded to avoid redundant downloads
- Creating necessary directory structures for data storage
- Downloading data from specified URLs
- Extracting compressed data files (tar.gz format)
"""

import os
import tarfile
import requests
import pandas as pd


class MovieDataAnalyzer:
    """Class for downloading and analyzing movie data."""

    def __init__(self) -> None:
        """
        Initialize the MovieDataAnalyzer class.

        Args:
            data_url: URL of the data file to download
        """
        # Set the data URL
        data_url = 'http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz'

        # Set the download directory
        download_dir: str = '../downloads'

        # Create the download directory if it doesn't exist
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            print(f"Created download directory: {download_dir}")
        else:
            print(f"Download directory already exists: {download_dir}")

        # Download if file does not exist in the download directory
        tar_file_name = os.path.basename(data_url) # Extract the file name from the URL
        tar_path = os.path.join(download_dir, tar_file_name)
        file_name = os.path.splitext(os.path.splitext(tar_file_name)[0])[0]
        dir_path: str = os.path.join(download_dir, file_name)
        if not os.path.exists(dir_path):
            # Download the file
            response = requests.get(data_url, stream=True, timeout=30)
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
            print(f"File {os.path.basename(dir_path)} already exists in the download directory.")

        # Read the datasets into corresponding dataframes
        self.movie_metadata = None
        self.character_metadata = None
        self.name_clusters = None
        self.plot_summaries = None
        self.tvtropes_clusters = None

        # Read each TSV file and create a DataFrame
        for file in os.listdir(dir_path):
            if file == "character.metadata.tsv":
                file_path = os.path.join(dir_path, file)
                ###
                #Column names from README:
                # 1. Wikipedia movie ID, 2. Freebase movie ID, 3. Movie release date,
                # 4. Character name, 5. Actor date of birth, 6. Actor gender,
                # 7. Actor height (in meters), 8. Actor ethnicity (Freebase ID),
                # 9. Actor name, 10. Actor age at movie release,
                # 11. Freebase character/actor map ID, # 12. Freebase character ID,
                # 13. Freebase actor ID
                ###
                df = pd.read_csv(file_path, sep="\t", names=[
                    "wikipedia_movie_id", "freebase_movie_id", "movie_release_date", 
                    "character_name", "actor_date_of_birth", "actor_gender", "actor_height", 
                    "actor_ethnicity", "actor_name", "actor_age_at_movie_release", 
                    "freebase_character_actor_map_id", "freebase_character_id", 
                    "freebase_actor_id"
                ], encoding="utf-8", on_bad_lines="skip")
                self.characters = df  # Store as an attribute
            elif file == "movie.metadata.tsv":
                file_path = os.path.join(dir_path, file)
                ###
                #Column names from README:
                # 1. Wikipedia movie ID, 2. Freebase movie ID, 3. Movie name, 4. Movie release date,
                # 5. Movie box office revenue, 6. Movie runtime,
                # 7. Movie languages (Freebase ID:name tuples),
                # 8. Movie countries (Freebase ID:name tuples),
                # 9. Movie genres (Freebase ID:name tuples)
                ###
                df = pd.read_csv(file_path, sep="\t", names=[
                    "wikipedia_movie_id", "freebase_movie_id", "movie_name", "movie_release_date", 
                    "movie_box_office_revenue", "movie_runtime", "movie_languages", 
                    "movie_countries", "movie_genres"
                ], encoding="utf-8", on_bad_lines="skip")
                self.movie_metadata = df  # Store as an attribute
            elif file == "name.clusters.txt":
                file_path = os.path.join(dir_path, file)
                ### Column names from README: 1. Name, 2. Actor ID
                df = pd.read_csv(file_path, sep="\t", names=["name", "actor_id"],
                                  encoding="utf-8", on_bad_lines="skip")
                self.name_clusters = df
            elif file == "plot_summaries.txt":
                ### Column names from README: 1. Wikipedia movie ID, 2. Plot summary
                file_path = os.path.join(dir_path, file)
                df = pd.read_csv(file_path, sep="\t", names=["movie_id", "summary"],
                                 encoding="utf-8", on_bad_lines="skip")
                self.plot_summaries = df  # Store as an attribute
            elif file == "tvtropes.clusters.txt":
                ### Column names from README: Cluster ID and Name
                file_path = os.path.join(dir_path, file)
                df = pd.read_csv(file_path, sep="\t", names=["name", "cluster"],
                                 encoding="utf-8", on_bad_lines="skip")
                self.tvtropes_clusters = df  # Store as an attribute
            else:
                print(f"File {file} does not match any expected data file.")
        print("All files have been loaded as DataFrame attributes.")

    def movie_type(self, N: int = 10) -> pd.DataFrame:
        """
        Calculate the N most common types of movies and their counts.

        Args:
            N (int): Number of top movie types to return. Default is 10.

        Returns:
            pd.DataFrame: DataFrame with columns "Movie_Type" and "Count" for the top N movie types.
        """
        if not isinstance(N, int):
            raise TypeError("N must be an integer")

        # Split the movie genres into individual genres
        genres = self.movie_metadata['movie_genres'].str.split(',').explode()

        # Count the occurrences of each genre
        genre_counts = genres.value_counts().head(N).reset_index()
        genre_counts.columns = ['Movie_Type', 'Count']

        return genre_counts

# Create an instance of the MovieDataAnalyzer class
analyzer = MovieDataAnalyzer()
