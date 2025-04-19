# Hybrid Movie Recommendation System

This project implements a hybrid movie recommender system that combines User-User Collaborative Filtering with Content-Based Filtering to generate personalized and novel movie suggestions. The system leverages user rating data along with movie metadata (such as genres) to create tailored recommendations that reflect both user preferences and movie content.



## Table of Contents
- [Project Overview](#project-overview)
- [How It Works](#How-It-Works)
- [Environment Preparation](#environment-preparation)
  - [Using Python Virtual Environment (venv)](#using-python-virtual-environment-venv)
  - [Using Conda](#using-conda)
- [Dependencies](#dependencies)
- [Running the Project](#Running-the-Project)
- [Contributors](#contributors)
- [License](#license)

## Project Overview

The goal of this system is to enhance user experience by intelligently recommending movies through a hybrid strategy:

- Collaborative Filtering captures user taste patterns based on other users’ preferences.
- Content-Based Filtering introduces diversity using movie attributes like genres.
- The final output is a ranked, deduplicated list of movie recommendations tailored to the user.


## How It Works

1. Data Loading
Loads multiple datasets including user ratings, movie metadata, genre encodings, and more (ratings.csv, tags.csv, Genres_encoded.csv, Films_metadata.csv, etc.).

2. Preprocessing
Cleans and merges data using movie IDs. Constructs:

 - A user-item (utility) matrix from rating data

 - A movie feature matrix using genre info

3. User-User Collaborative Filtering
Uses cosine similarity to find users with similar preferences and predict ratings for unseen movies.

4. Content-Based Filtering
Calculates similarity between movies based on genre vectors to recommend content-alike items.

5. Hybrid Merging
Combines recommendations from both methods, sorts them using global average rating, and trims to the requested number of suggestions.

6. Ranking & Deduplication
Ensures unique and relevant recommendations rise to the top.

7. Final Output
Returns a curated list of movie recommendations optimized for both personalization and discovery.

## Environment Setup
Choose either a Python virtual environment or Conda for setup:

### Using Python Virtual Environment (venv)
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  # or myenv\Scripts\activate on Windows
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

### Using Conda

    ```bash
    conda create --name myenv python=3.10
    conda activate myenv
    conda install numpy pandas scikit-learn matplotlib seaborn
    conda install -c conda-forge pyqt
    pip install scikit-surprise fastapi uvicorn pydantic requests
    ```

## Dependencies

The primary dependencies for this project are:
- PyQt5 (if using GUI components)
- NumPy / pandas for numerical and tabular data processing
- scikit-learn for machine learning utilities
- matplotlib / seaborn for data visualization
- scikit-surprise for collaborative filtering
- FastAPI / Uvicorn for web API support (if applicable)
- Pydantic / Requests for data handling and HTTP

## Runnning the Project

After setting up your environment, you can run your main application script.
    ```bash
    python main.py
    ```
Make sure to replace main.py with the actual entry point script in your project.

## Contributing

Contributions are welcome! Feel free to fork the repository, make improvements, and open a pull request. For significant changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
