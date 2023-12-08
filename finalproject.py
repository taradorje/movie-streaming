#########################################
##### Name: Tara Dorje              #####
##### Uniqname: tydorje             #####
#########################################

import requests
import json

TMDb_key = "INSERT"
StreamingAvailability_key = "INSERT"

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

def get_streaming_link_from_cache(tmdb_id, service):
    '''retrieves the streaming link from the cache for a specified TMDb ID and service

    opens the cache, checks if streaming link info is available for a service, and returns the link if available. else, returns None.

    Parameters
    ----------
    tmdb_id : int
        the TMDb ID of the movie
    service : str
        the streaming service for which the link is being retrieved

    Returns
    -------
    str or None
        the streaming link, if available, or None if not found in the cache
    '''
    cache = open_cache() # open the cache
    streaming_links = cache[str(tmdb_id)]["streaming_link"] # get streaming links info

    if service in streaming_links: # if service is represented in streaming links info,
        return streaming_links[service] # return the streaming link

    return None # else, return None

#################FUNCTIONS###############

def print_services():
    ''' prints a list of available streaming services

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    print("Available Streaming Services:")

    for index, service in enumerate(services, start=1):
        print(f"[{index}] {service}")
    
    print()

def print_languages():
    ''' prints a list of available languages

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    print("Available Languages:")

    for index, language in enumerate(languages, start=1):
        print(f"[{index}] {language}")
    
    print()

def print_genres():
    ''' prints a list of available genres

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    print("Available Genres:")

    for index, genre in enumerate(genres, start=1):
        print(f"[{index}] {genre}")
    
    print()

def print_durations():
    ''' prints a list of available movie durations
    
    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    print("Available Movie Durations: ")

    for index, duration in enumerate(durations, start=1):
        print(f"[{index}] {duration}")
    
    print()

def get_tmdb_watch_provider(user_service):
    ''' gets the TMDb watch provider ID for the user-specified streaming service

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
    ''' makes a request to the StreamingAvailabilityAPI, updates the cache, and returns the retrieved streaming link

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
    url = "https://streaming-availability.p.rapidapi.com/get"

    querystring = {"output_language":"en","tmdb_id":f"movie/{tmdb_id}"}

    headers = {
        "X-RapidAPI-Key": StreamingAvailability_key,
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    result = response.json().get("result", {})

    if "streamingInfo" in result and "us" in result["streamingInfo"]:
        services = result["streamingInfo"]["us"]

        for service in services:
            if service["service"] == get_streaming_availability_service(user_service): # if user-specified service is available,
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

###################MAIN##################

if __name__ == "__main__":
    while True:
        print("//// Welcome to the Movie-Streaming Generator \\\\\\\\\n")

        services = ["Netflix", "Prime", "Disney", "HBO Max", "Hulu", "Peacock", "Paramount", "Starz", "Showtime", "Apple TV", "MUBI"]
        genres = ["Adventure","Fantasy","Animation","Drama","Horror","Action","Comedy","History","Western","Thriller","Crime","Documentary","Science Fiction","Mystery","Music","Romance","Family","War"]
        durations = ["Short (< 89 min)", "Medium (90–120 min)", "Long (> 120 min)"]
        languages = ["English", "French", "German", "Spanish", "Hindi", "Mandarin", "Japanese", "Korean"]

        #################SERVICE#################

        print_services()
        while True:
            user_service = input("Please enter the number of your preferred streaming service: ")
            if user_service.isdigit() and 1 <= int(user_service) <= len(services):
                break
            else:
                print(f"Invalid input. Please enter a number between 1 and {len(services)}.")
        user_service = services[int(user_service) - 1]
        print(f"Your preferred streaming service is: {user_service}\n")

        #################LANGUAGE################

        print_languages()
        while True:
            user_language = input("Please enter your preferred movie language: ")
            if user_language.isdigit() and 1 <= int(user_language) <= len(languages):
                break
            else:
                print(f"Invalid input. Please enter a number between 1 and {len(languages)}.")
        user_language = languages[int(user_language) - 1]
        print(f"Your preferred movie language is: {user_language}\n")

        ##################GENRE##################

        print_genres()
        while True:
            user_genre = input("Please enter the number of your preferred movie genre: ")
            if user_genre.isdigit() and 1 <= int(user_genre) <= len(genres):
                break
            else:
                print(f"Invalid input. Please enter a number between 1 and {len(genres)}.")
        user_genre = genres[int(user_genre) - 1]
        print(f"Your preferred movie genre is: {user_genre}\n")

        #################DURATION################

        print_durations()
        runtime_gte = 0 # runtime greater than or equal to
        runtime_lte = 10000 # runtime less than or equal to
        while True:
            user_duration = input("Please enter the number of your preferred movie duration: ")
            if user_duration.isdigit() and 1 <= int(user_duration) <= len(durations):
                if int(user_duration) == 1:
                    runtime_lte = 89
                elif int(user_duration) == 2:
                    runtime_gte = 90
                    runtime_lte = 120
                elif int(user_duration) == 3:
                    runtime_gte = 121
                break
            else:
                print(f"Invalid input. Please enter a number between 1 and {len(durations)}.")
        print(f"Your preferred movie duration is: {durations[int(user_duration) - 1]}\n")

        ##################SEARCH################

        service_id = get_tmdb_watch_provider(user_service)
        genre_id = get_tmdb_genre_id(user_genre)
        language_id = get_tmdb_language_id(user_language)

        cache_key = f"{service_id}_{genre_id}_{language_id}_{runtime_gte}_{runtime_lte}"
        tmdb_ids = tmdb_discover_movie_cached(cache_key, service_id, genre_id, language_id, runtime_gte, runtime_lte)

        results = 0
        result_ids = []

        if len(tmdb_ids) == 0:
            user_search_again = input("No films matching your criteria available. Would you like to search again? (y/n) ")
            if user_search_again.lower() == "y":
                continue
            else:
                break
        else:
            for tmdb_id in tmdb_ids:
                movie = tmdb_movie_details(tmdb_id)
                if runtime_gte <= movie["runtime"] <= runtime_lte: # account for any incorrect runtime input in TMDb Discover Movie endpoint
                    results += 1
                    result_ids.append(tmdb_id)
                    print(results)
                    print(f"Title: {movie['title']}")
                    print(f"Director(s): {', '.join(tmdb_directors(tmdb_id))}")
                    print(f"Runtime: {movie['runtime']} min.")
                    print(f"Genre: {user_genre}")
                    print(f"Language: {user_language}")
                    print(f"Streaming Service: {user_service}")
                    if movie['poster_path']:
                        print(f"Poster: https://image.tmdb.org/t/p/original/{movie['poster_path']}")
                    print(f"Synopsis: {movie['overview']}")
                    print()
        
        if results == 0: # account for any incorrect runtime input in TMDb Discover Movie endpoint
            user_search_again = input("No films matching your criteria available. Would you like to search again? (y/n) ")
            if user_search_again.lower() == "y":
                continue
            else:
                break
        
        else:
            while True:
                user_input = input("Please select a movie number from the list: ")
                if user_input.isdigit():
                    user_selection = int(user_input)
                    if 1 <= user_selection <= results: # check for valid user selection
                        user_selection = result_ids[user_selection - 1]
                        streaming_link = get_streaming_link_from_cache(user_selection, user_service) # check cache for existing streaming link

                        if streaming_link: # if streaming link in cache,
                            print(f"{streaming_link}") # print streaming link
                        else: # if streaming link not in cache,
                            streaming_link = get_streaming_link(user_selection, user_service) # make request to StreamingAvailabilityAPI
                            if streaming_link: # if streaming link is valid,
                                print(streaming_link) # print valid streaming link
                            else: # if no streaming link,
                                print("Streaming link not available.") # print missing link message
                            update_cache_with_streaming_link(user_selection, user_service, streaming_link) # update the cache with the retrieved streaming link
                        user_response = input("Would you like to select another movie? (y/n) " )
                        if user_response.lower() == "y":
                            pass
                        else:
                            break
                    else:
                        print(f"Invalid input. Please enter a number between 1 and {results}.")
                else:
                    print("Invalid input. Please enter a valid number.")
            break