#########################################
##### Name: Sasha Kenkre            #####
##### Uniqname: skenkre             #####
#########################################

import json
import requests
import webbrowser

class Media:

    """
    A class to represent Media.


    Attributes
    ----------
    title (str): title of media
    author (str): author of media
    release_year (str): year media was released
    url (str): web url to access media content
    json (dict): dictionary with information about artist

    Methods
    -------
    info(): Returns title, author, and release year of media.
    length(): Returns 0
    """

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):

        """
        Constructs all the necessary attributes for the media object.

        Parameters
        ----------
        title (str): title of media
        author (str): author of media
        release_year (str): year media was released
        url (str): web url to access media content
        json (dict): dictionary with information about artist
        """

        if json is not None:
            try:
                self.title = json['trackName']
            except:
                self.title = json['collectionName']
            self.author = json['artistName']
            self.release_year = json['releaseDate'][:4]
            if 'trackViewUrl' in json:
                self.url = json['trackViewUrl']
            else:
                self.url = json['collectionViewUrl']
        else:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

    def info(self):
        """
        Returns a string with title, author, and release year of media.

        Parameters
        ----------
        None

        Returns
        ----------
        Returns a string with title, author, and release year of media.
        """
        return f"{self.title} by {self.author} ({self.release_year})"

    def length(self):
        """
        Returns the length of media (default 0).

        Parameters
        ----------
        None

        Returns
        ----------
        Returns the length of media (default 0).
        """
        return 0

# Other classes, functions, etc. should go here

class Song(Media):

    """
    A class to represent a Song, inherits instances from Media class.


    Attributes
    ----------
    title (str): title of song
    author (str): author of song
    release_year (str): year song was released
    url (str): web url to access song content
    album (str): album name
    genre (str): song genre
    track_length (int): length of song
    json (dict): dictionary with information about artist

    Methods
    -------
    info(): Returns title, author, release year, and genre of song.
    length(): Returns track_length in seconds.
    """
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album="No Album", genre="No Genre", track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is not None:
            self.album = json["collectionName"]
            self.track_length = int(json["trackTimeMillis"])
            self.genre = json["primaryGenreName"]
        else:
            self.album = album
            self.genre = genre
            self.track_length = track_length

    def info(self):
        """
        Returns a string with title, author, release year, and genre of song.

        Parameters
        ----------
        None

        Returns
        ----------
        Returns title, author, release year, and genre of song.
        """

        return super().info() + f" [{self.genre}]"

    def length(self):
        """
        Returns the length of song in seconds.

        Parameters
        ----------
        None

        Returns
        ----------
        Returns the length of song in seconds.
        """

        return int((int(self.track_length) / 1000)) #convert to seconds from milliseconds

class Movie(Media):
    """
    A class to represent a Movie, inherits instances from Media class.


    Attributes
    ----------
    title (str): title of song
    author (str): author of song
    release_year (str): year song was released
    url (str): web url to access song content
    rating (str): movie rating
    movie_length (int): length of movie
    json (dict): dictionary with information about artist

    Methods
    -------
    info(): Returns title, author, release year, and rating of movie.
    length(): Returns movie_length in minutes.
    """

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating="No Rating", movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is not None:
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = int(json["trackTimeMillis"])
        else:
            self.rating = rating
            self.movie_length = movie_length

    def info(self):
        """
        Returns a string with title, author, release year, and rating of movie.

        Parameters
        ----------
        None

        Returns
        ----------
        Returns title, author, release year, and rating of song.
        """

        return super().info() + f" [{self.rating}]"

    def length(self):
        """
        Returns the length of movie in minutes.

        Parameters
        ----------
        None

        Returns
        ----------
        Returns the length of movie in minutes.
        """

        return int((int(self.movie_length) / 60000)) # convert to minutes from milliseconds, round to nearest minute


def get_data(artist, limit):
    """
    Returns a dictionary from iTunes API for an artist with the number of results you want.

    Parameters
    ----------
        artist (str): name of artist/movie/other media
        limit (int): number of results for search

    Returns
    ----------
        artist_info (dict): A dictionary with artist information with a specified limit of results
    """

    params = {
        'term': artist,
        'limit': limit
    }
    response = requests.get("https://itunes.apple.com/search?", params=params)
    artist_info = json.loads(response.text)
    return artist_info

# beatles = get_data('The Beatles', 3)
# print(type(beatles))
# print(beatles['results'])

def get_results(name):
    """
    Gets information regarding the artist/movie/other media requested by the user.

    Parameters:
        name (str): name of artist/movie/other media inputted by user.

    Returns:
        None
    """

    num_media = 0
    while True:
        num_results_str = input("How many results do you want to preview? ")
        try:
            num_results = int(num_results_str)
        except:
            print("Please enter a valid number greater than 0.")
            continue
        if num_results < 1 or num_results > 50:
            print("Please enter a valid number between 1 and 50, inclusive.")
            continue
        break
    results = get_data(name, num_results)
    print(f"\nSONGS")
    num_song = 0
    for result in results['results']:
        if result['wrapperType'] == 'track':
            if 'song' in result['kind']:
                num_media += 1
                num_song += 1
                print(f"{str(num_media)} {Song(json=result).info()}")
                media_list.append(result)
    if num_song < 1:
        print('There are no songs that match your search.')

    print(f"\nMOVIES")
    num_movie = 0
    for result in results['results']:
        if result['wrapperType'] == 'track':
            if 'feature-movie' in result['kind']:
                num_media += 1
                num_movie += 1
                print(f"{str(num_media)} {Movie(json=result).info()}")
                media_list.append(result)
    if num_movie < 1:
        print('There are no movies that match your search.')

    print(f"\nOTHER MEDIA")
    num_other_media = 0
    for result in results['results']:
        if result['wrapperType'] == 'track':
            if 'song' not in result['kind']:
                if 'feature-movie' not in result['kind']:
                    num_media += 1
                    num_other_media += 1
                    print(f"{str(num_media)} {Media(json=result).info()}")
                    media_list.append(result)
        elif result['wrapperType'] != 'track':
            num_media += 1
            num_other_media += 1
            print(f"{str(num_media)} {Media(json=result).info()}")
            media_list.append(result)

    if num_other_media < 1:
        print(f"There is no other media that matches your search.\n")

    if num_media < 1:
        print(f"There are no results for your search.")



if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    media_list = []
    info = ''
    while True:
        if len(media_list) == 0:
            term = input('Enter a search term, or "exit" to quit: ')
            if term == 'exit':
                print('Bye!')
                break
            else:
                get_results(term)
        else:
            info = input('Enter a number for more info, or another search term, or "exit": ')
            if info == 'exit':
                print('Bye!')
                break
            try:
                num = int(info)
                print("Launching")
                if 'trackViewUrl' in media_list[num-1]:
                    print(media_list[num-1]['trackViewUrl'])
                    print(f"in web browser...")
                    webbrowser.open(media_list[num-1]['trackViewUrl'])
                else:
                    print(media_list[num-1]['collectionViewUrl'])
                    print(f"in web browser...")
                    webbrowser.open(media_list[num-1]['collectionViewUrl'])
            except:
                media_list = []
                get_results(info)

