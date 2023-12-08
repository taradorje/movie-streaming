# MOVIE STREAMING APP

A final project for SI 507 at the University of Michigan.

## Requirements

Required Packages: requests, flask
Required API Keys: TMDb API, StreamingAvailabilityAPI (RapidAPI)

TMDb API Documentation + API Key Access: https://developer.themoviedb.org/reference/intro/getting-started
StreamingAvailabilityAPI Documentation + API Key Access: https://www.movieofthenight.com/about/api/documentation

## Demo Videos

Flask Demo Video: https://www.youtube.com/watch?v=hJH6KS2QNfw
Command-Line Interface Demo Video: https://www.youtube.com/watch?v=RPLiwyMkaac

## Instructions (Flask)

1. Register for API keys from TMDb API and StreamingAvailabilityAPI (RapidAPI)
2. Define API keys in app.py
3. Install Flask using pip install Flask
4. Launch Flask site by running python3 app.py
5. Select preferences from service, genre, language, and duration dropdowns, then click "Search"
6. Browse list of movie results, then click on "Get Streaming Link" for a desired film
7. You will be redirected to the streaming link on your requested platform, if available, or taken to a "Streaming Link Not Available" page prompting you to return to the list of search results

## Overview

A program that asks users to specify movie criteria, including genre, language, duration, and preferred streaming platform. The program then searches for movies that fit their specified criteria by accessing movie data from the TMDb API and returning the appropriate results. From there, users can make a selection from the list of available movies, which are displayed with relevant details such as Title, Director(s), Runtime, Overview, etc., as well as a poster image. Once a user makes a selection from the list of returned films by clicking on the "Get Streaming Link" button, the program accesses additional streaming data from the StreamingAvailabilityAPI, which directly links users to the appropriate movie page on their selected streaming platform. If there are any gaps in StreamingAvailabilityAPI's data, users are directed to a "Streaming Link Not Available" page that prompts them to return to their search results and make a new selection. Caching is implemented to store raw JSON results from both APIs, reducing the need for repeated requests and improving overall program efficiency. Since the TMDb Discover endpoint alone does not provide certain key movie information such as Director(s) and also requires input of set TMDb Genre, Language, and Watch Provider IDs (as opposed to name strings), the program requires accessing the TMDb Details, Credits, Genres, Languages, and Watch Providers endpoints to retrieve all necessary information.

## Data Structure

The program data is organized into a tree data structure that can be viewed in the "cache.json" file. The file is built through multiple requests to TMDb API and StreamingAvailabilityAPI. It is structured to contain the parameters used in the Discover Movie endpoint that returns TMDb IDs as its cache keys. It is also structured to contain individual movies’ TMDb IDs as cache keys, with their associated details as values, including a streaming link for any user-specified services. A cache key such as “8_16_en_90_120” denotes specified movie preferences by the user (e.g. genre_id, service, runtime, language), and returns a list of TMDb IDs that fit the user’s criteria. As for cache keys that are TMDb IDs, each of their values are initially constructed through calls to the TMDb Details and Credits endpoints to retrieve additional movie data, but they are also updated as needed with a streaming link from StreamingAvailabilityAPI when “Get Streaming Link” is requested by the user.

The tree structure is organized by the user’s preferences and responses to the initial series of questions presented by the main page of the program. These responses guide the program in forming a hierarchical structure that leads to personalized movie recommendations. The tree nodes represent different decision configurations that lead to specific movie recommendations, based on user criteria. My program traverses the cache dictionary structure's information, retrieved from TMDb API and StreamingAvailability API. User responses to the initial set of questions guide the program’s selection of nodes and branches, ultimately leading to a set of recommended movies tailored to the user’s specified criteria and desired streaming platform.
