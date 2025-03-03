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
Example:
    analyzer = MovieDataAnalyzer('https://example.com/movie_data.tar.gz')
"""

import os
import tarfile
import requests


class MovieDataAnalyzer:
    """Class for downloading and analyzing movie data."""

    def __init__(self, data_url: str) -> None:
        """
        Initialize the MovieDataAnalyzer class.

        Args:
            data_url: URL of the data file to download
        """
        # Set the download directory
        self.download_dir: str = '../downloads'

        # Set the file path
        filename: str = 'MovieSummaries'
        self.file_path: str = os.path.join(self.download_dir, filename)

        # Create the download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        # Download the file if it doesn't exist
        if not os.path.exists(self.file_path):
            print("Downloading Data...")
            self._download_file(data_url)
        else:
            print(f"File {filename} already exists. Skipping download.")

    def _download_file(self, url: str) -> None:
        """
        Download and extract the file from the provided URL.
        
        Args:
            url: The URL to download the file from
        """
        # Download the file
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(self.file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print("Download complete.")

        # Extract the tarball
        print(f"Extracting {os.path.basename(self.file_path)}...")
        with tarfile.open(self.file_path, 'r:gz') as tar:
            tar.extractall(path=self.download_dir)
        print("Extraction complete.")
