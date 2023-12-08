#########################################
##### Name: Tara Dorje              #####
##### Uniqname: tydorje             #####
#########################################

from flask import Flask, render_template, request, redirect, url_for

import requests
import json

TMDb_key = "INSERT"
StreamingAvailability_key = "INSERT"

app = Flask(__name__)

##################CACHE##################

CACHE_FILE = "cache.json"

def open_cache():
    ''' opens the cache file if it exists and loads the JSON data into a dictionary

    if the cache file doesn't exist, creates a new cache dictionary.
    
    Parameters
    ----------
    none

    Returns
    -------
    dict
        the opened cache as a dictionary
    '''
    try:
        with open(CACHE_FILE, 'r') as cache_file:
            cache_contents = cache_file.read()
            return json.loads(cache_contents) if cache_contents else {}
    except:
        return {}

def save_cache(cache):
    ''' saves the provided cache dictionary to the cache file in JSON format

    cache dictionary is saved to the designated CACHE_FILE.

    Parameters
    ----------
    cache: dict
        the cache dictionary that needs to be saved

    Returns
    -------
    none
    '''
    with open(CACHE_FILE, 'w') as cache_file:
        json.dump(cache, cache_file)

def update_cache(cache_key, data):
    ''' updates the cache with the specified cache key and data from TMDb Discover Movie endpoint

    Parameters
    ----------
    cache_key : str
        the key to identify the data in the cache
    data : dict
        the movie data to be stored in the cache

    Returns
    -------
    none
    '''
    cache = open_cache() # open the cache
    cache[cache_key] = data # update the cache key with data
    save_cache(cache) # save the cache

def update_cache_with_movie_details(tmdb_id, movie_details):
    ''' updates the cache with movie details for a specific TMDb ID from the TMDb Details endpoint

    Parameters
    ----------
    tmdb_id : int
        the TMDb ID of the movie
    movie_details : dict
        the details of the movie to be stored in the cache

    Returns
    -------
    none
    '''
    cache = open_cache() # open the cache
    cache[tmdb_id] = {"movie_details": movie_details, "streaming_link": {}} # update the cache with movie details
    save_cache(cache) # save the cache

def get_movie_details_from_cache(tmdb_id):
    ''' retrieves movie details from the cache for a specific TMDb ID

    Parameters
    ----------
    tmdb_id : int
        the TMDb ID of the movie

    Returns
    -------
    dict or None
        the movie details if found in the cache, otherwise None
    '''
    cache = open_cache() # open the cache
    cache_key = str(tmdb_id) # define a cache key

    if cache_key in cache: # if cache key already in cache,
        return cache[cache_key]["movie_details"] # return the movie details from the cache

    return None # else, return None

def tmdb_discover_movie_cached(cache_key, service, genre, original_language, runtime_gte, runtime_lte):
    ''' either retrieves data from the cache or makes a request to the TMDb Discover Movie endpoint, updates the cache, and returns the retrieved data

    Parameters
    ----------
    cache_key : str
        the cache key used to identify the cached data
    service : str
        the TMDb ID for the movie's streaming service
    genre : str
        the TMDb ID for the movie's genre
    original_language : str
        the TMDb for the movie's original language
    runtime_gte : int
        the minimum runtime of the movie
    runtime_lte : int
        the maximum runtime of the movie
    
    Returns
    -------
    dict
        the cached data, if available. otherwise, the retrieved data from the TMDb Discover Movie endpoint
    '''
    cache = open_cache() # open the cache
    cached_data = cache.get(cache_key) # get the cached data

    if cached_data: # if data is found in cache,
        return cached_data # return the cached data

    data = tmdb_discover_movie(service, genre, original_language, runtime_gte, runtime_lte) # if no  data found in cache, make a request to the TMDb Discover Movie endpoint
    update_cache(cache_key, data) # update the cache
    return data # return the retrieved data

def update_cache_with_streaming_link(tmdb_id, service, streaming_link):
    '''updates cache with streaming link for a specified TMDb ID and service
    
    opens the cache, updates it with a streaming link for a service, then saves the cache.

    Parameters
    ----------
    tmdb_id : int
        the TMDb ID of the movie
    service : str
        the streaming service for which the link is being updated
    streaming_link : str
        the streaming link to be stored in the cache

    Returns
    -------
    none
    '''
    cache = open_cache() # open the cache
    cache[str(tmdb_id)]["streaming_link"][service] = streaming_link # check for existing streaming link

    if streaming_link: # if streaming link available,
        cache[str(tmdb_id)]["streaming_link"][service] = streaming_link # update cache with streaming link
    else: # if streaming link not available,
        cache[str(tmdb_id)]["streaming_link"][service] = "Streaming link not available." # update cache with missing link info
    
    save_cache(cache) # save the updates to the cache

def get_streaming_link_from_cache(tmdb_id, user_service):
    '''retrieves the streaming link from the cache for a specified TMDb ID and service

    opens the cache, checks if streaming link info is available for a service, and returns the link if available. else, returns None.

    Parameters
    ----------
    tmdb_id : int
        the TMDb ID of the movie
    user_service : str
        the streaming service for which the link is being retrieved

    Returns
    -------
    str or None
        the streaming link, if available, or None if not found in the cache
    '''
    cache = open_cache() # open the cache
    streaming_links = cache[str(tmdb_id)]["streaming_link"] # get streaming links info

    if user_service in streaming_links: # if service is represented in streaming links info,
        return streaming_links[user_service] # return the streaming link

    return None # else, return None

#################FUNCTIONS###############

def get_tmdb_watch_provider(user_service):
    ''' gets the TMDb watch provider ID for the specified streaming service

    Parameters
    ----------
    user_service : str
        the name of the streaming service

    Returns
    -------
    int
        the TMDb watch provider ID
    '''
    url = "https://api.themoviedb.org/3/watch/providers/movie?language=en-US&watch_region=US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDb_key}"
    }

    params={
        "api_key": TMDb_key
    }

    response = requests.get(url, headers=headers, params=params)
    providers = response.json().get("results", [])

    for provider in providers:
        if provider["provider_name"] == user_service:
            return provider["provider_id"]

def get_tmdb_genre_id(user_genre):
    ''' gets the TMDb genre ID for the user-specified genre

    Parameters
    ----------
    user_genre : str
        the name of the genre

    Returns
    -------
    int
        the TMDb genre ID
    '''
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDb_key}"
    }

    params={
        "api_key": TMDb_key
    }

    response = requests.get(url, headers=headers, params=params)
    genres = response.json().get("genres", [])

    for genre in genres:
        if genre["name"] == user_genre:
            return genre["id"]

def get_tmdb_language_id(user_language):
    ''' gets the TMDb language ID for the user-specified language

    Parameters
    ----------
    user_language : str
        the name of the language

    Returns
    -------
    int
        the TMDb language ID
    '''
    url = "https://api.themoviedb.org/3/configuration/languages"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDb_key}"
    }

    params={
        "api_key": TMDb_key
    }

    response = requests.get(url, headers=headers, params=params)
    languages = response.json()

    for language in languages:
        if language["english_name"] == user_language:
            return language["iso_639_1"]

def tmdb_discover_movie(service, genre, original_language, runtime_gte, runtime_lte, language="en-US"):
    ''' makes a request to the TMDb Discover Movie endpoint based on user-specified criteria

    Parameters
    ----------
    service : str
        the TMDb watch provider ID for filtering
    genre : int
        the TMDb genre ID for filtering
    original_language : str
        the TMDb language ID for filtering
    runtime_gte : int
        the minimum runtime (in minutes) for filtering
    runtime_lte : int
        the maximum runtime (in minutes) for filtering
    language : str, optional
        the language for movie details results (default of "en-US")

    Returns
    -------
    list
        a list of TMDb IDs for movies that match the criteria
    '''
    url = "https://api.themoviedb.org/3/discover/movie"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDb_key}"
    }

    params={
        "api_key": TMDb_key,
        "include_adult": "false",
        "include_video": "false",
        "language": language,
        "with_genres": genre,
        "with_original_language": original_language,
        "with_runtime.gte": runtime_gte,
        "with_runtime.lte": runtime_lte,
        "watch_region": "US",
        "with_watch_providers": service
    }

    response = requests.get(url, headers=headers, params=params)
    results = response.json().get("results", [])

    return [result["id"] for result in results]

def tmdb_movie_details(tmdb_id):
    ''' makes a request to the TMDb Details endpoint for a specific movie

    Parameters
    ----------
    tmdb_id : int
        the TMDb ID of the movie

    Returns
    -------
    dict
        a dictionary containing movie details
    '''
    cached_details = get_movie_details_from_cache(tmdb_id) # check cache for movie details

    if cached_details: # if cache already contains movie details,
        return cached_details # return cached data
    
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDb_key}"
    }

    params={
        "api_key": TMDb_key,
        "language": "en-US"
    }

    response = requests.get(url, headers=headers, params=params) # if no data found in cache, make a request to TMDb Details endpoint
    data = response.json()

    update_cache_with_movie_details(tmdb_id, data) # update the cache
    return data # return the retrieved data

def tmdb_directors(tmdb_id):
    ''' makes a request to the TMDb Credits endpoint to get the Director(s) for a specific movie

    Parameters
    ----------
    tmdb_id : int
        the TMDb ID of the movie

    Returns
    -------
    list
        a list of directors for the movie, or a list containing "Unknown" if no crew and/or directors
    '''
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDb_key}"
    }

    params={
        "api_key": TMDb_key,
        "language": "en-US"
    }

    response = requests.get(url, headers=headers, params=params)
    crew = response.json().get("crew", [])
    if not crew: # if no crew data available,
        return ["Unknown"] # return Unknown director
    directors = [member["name"] for member in crew if member["job"] == "Director"]
    if not directors: # if no director data available,
        return ["Unknown"] # return Unknown director
    return directors # return the list of directors
        
def get_streaming_link(tmdb_id, user_service):
    ''' either retrieves data from the cache or makes a request to the StreamingAvailabilityAPI, updates the cache, and returns the retrieved streaming link

    Parameters
    ----------
    tmdb_id : int
        the TMDb ID of the movie
    user_service : str
        the preferred streaming service

    Returns
    -------
    str or None
        the streaming link, if available. otherwise, returns None
    '''
    cached_details = get_streaming_link_from_cache(tmdb_id, user_service) # check cache for streaming link

    if cached_details: # if streaming link in cache,
        return cached_details # return cached streaming link
    
    url = "https://streaming-availability.p.rapidapi.com/get"

    querystring = {"output_language":"en","tmdb_id":f"movie/{tmdb_id}"}

    headers = {
        "X-RapidAPI-Key": StreamingAvailability_key,
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring) # else, make a request to StreamingAvailabilityAPI
    result = response.json().get("result", {})

    if "streamingInfo" in result and "us" in result["streamingInfo"]:
        services = result["streamingInfo"]["us"]

        for service in services:
            if service["service"] == get_streaming_availability_service(user_service): # if user-specified service is available,
                update_cache_with_streaming_link(tmdb_id, user_service, service["link"]) # update cache with retrieved streaming link
                return service["link"] # return streaming link

    return None

def get_streaming_availability_service(user_service):
    ''' gets the corresponding StreamingAvailabilityAPI service code for the given streaming service

    Parameters
    ----------
    user_service : str
        the name of the streaming service

    Returns
    -------
    str
        the corresponding StreamingAvailabilityAPI service code
    '''
    service_mappings = {
        "Netflix": "netflix",
        "Prime": "prime",
        "Disney": "disney",
        "HBO Max": "hbo",
        "Hulu": "hulu",
        "Peacock": "peacock",
        "Paramount": "paramount",
        "Starz": "starz",
        "Showtime": "showtime",
        "Apple TV": "apple",
        "MUBI": "mubi",
    }
    return service_mappings[user_service]

##################FLASK##################

@app.route('/')
def index():
    services = ["Netflix", "Prime", "Disney", "HBO Max", "Hulu", "Peacock", "Paramount", "Starz", "Showtime", "Apple TV", "MUBI"] # initialize values for streaming service dropdown
    genres = ["Adventure","Fantasy","Animation","Drama","Horror","Action","Comedy","History","Western","Thriller","Crime","Documentary","Science Fiction","Mystery","Music","Romance","Family","War"] # initialize values for genre dropdown
    languages = ["English", "French", "German", "Spanish", "Hindi", "Mandarin", "Japanese", "Korean"] # initialize values for language dropdown
    durations = ["Short (< 89 min)", "Medium (90–120 min)", "Long (> 120 min)"] # initialize values for durations dropdown

    return render_template("index.html", services=services, genres=genres, durations=durations, languages=languages) # render index.html

@app.route("/search", methods=["POST"])
def search():
    user_service = request.form.get("service") # retrieve form service data
    user_language = request.form.get("language") # retrieve form language data
    user_genre = request.form.get("genre") # retrieve form genre data
    user_duration = request.form.get("duration") # retrieve form duration data

    if user_duration == "Short (< 89 min)": # short films
        runtime_gte = 0 # runtime greater than or equal to 0
        runtime_lte = 89 # runtime less than or equal to 89
    elif user_duration == "Medium (90–120 min)": # medium films
        runtime_gte = 90 # runtime greater than or equal to 90
        runtime_lte = 120 # runtime less than or equal to 120
    elif user_duration == "Long (> 120 min)": # long films
        runtime_gte = 121 # runtime greater than or equal to 121
        runtime_lte = 10000  # runtime less than or equal to 10,000

    service_id = get_tmdb_watch_provider(user_service) # get TMDb watch provider ID
    genre_id = get_tmdb_genre_id(user_genre) # get TMDb genre ID
    language_id = get_tmdb_language_id(user_language) # get TMDb original language ID

    cache_key = f"{service_id}_{genre_id}_{language_id}_{runtime_gte}_{runtime_lte}" # generate Discover Movie endpoint cache key
    tmdb_ids = tmdb_discover_movie_cached(cache_key, service_id, genre_id, language_id, runtime_gte, runtime_lte) # get list of TMDb IDs from Discover Movie endpoint
    results = [] # initialize list of movie results

    for tmdb_id in tmdb_ids:
        movie = tmdb_movie_details(tmdb_id) # get additional movie details from Details endpoint
        if runtime_gte <= movie["runtime"] <= runtime_lte: # account for any incorrect runtime input in TMDb Discover Movie endpoint
            result = {
                "tmdb_id": tmdb_id,
                "title": movie["title"],
                "directors": ", ".join(tmdb_directors(tmdb_id)), # get directors from Credits endpoint
                "runtime": movie["runtime"],
                "genre": user_genre,
                "language": user_language,
                "service": user_service,
                "poster_path": f"https://image.tmdb.org/t/p/original/{movie['poster_path']}" if movie['poster_path'] else None,
                "overview": movie["overview"],
                "streaming_link": "" # initialize streaming link attribute for later use
            }
            results.append(result)

    return render_template("results.html", results=results) # render results.html with results

@app.route("/open_streaming_link", methods=["POST"])
def open_streaming_link():
    tmdb_id = request.form.get("tmdb_id") # retrieve form tmdb_id data
    user_service = request.form.get("service") # retrieve form service data

    streaming_link = get_streaming_link(tmdb_id, user_service) # retrieve streaming link either from cache or API

    if streaming_link and streaming_link != "Streaming link not available.": # if streaming link is available,
        return redirect(streaming_link) # redirect to the streaming link
    else: # else if streaming link is not available,
        return render_template("open_streaming_link.html", streaming_link=streaming_link) # render open_streaming_link.html with streaming link

if __name__ == '__main__':
    app.run(debug=True)