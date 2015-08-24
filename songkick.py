__author__ = 'DKeinan'
import requests
import logging
logging.basicConfig(filename='testing.log', filemode='w', format='%(message)s',level=logging.INFO)


class Songkick(object):

    """
    A Songkick object manages the calls to the Songkick API, finding and returning information based on parameters.
    Attributes:
        key: The required API key to make requests to the Songkick API.
    """

    def __init__(self, key):
        """
        Initializes the Songkick object and sets the 'key' attribute.
        Paramaters: A valid Songkick API key.
        """
        self.api_key = key

    def get_artist_info_by_name(self, name):
        """
        Queries Songkick 'Artist Search' with string 'name' for a valid artist name.
        Raises a ValueError if name string is empty.

        If no results are found, returns None.
        If any results are found, using the FIRST result, creates and returns an ArtistResponseObject.

        Paramaters:
            name: A string to be used as a query for an artist search.
        """

        if not name:
            raise ValueError("Invalid argument. Can't search with empty query.")

        logging.info('SK: Searching for artist name with query %s...', name)

        payload = {'query': name, 'apikey': self.api_key}
        r = requests.get("http://api.songkick.com/api/3.0/search/artists.json?", params=payload)
        data = r.json()
        num_results = int(data["resultsPage"]["totalEntries"])

        if num_results != 0:
            logging.info('SK: %d artist results found.', num_results)

            artist_name = data["resultsPage"]["results"]["artist"][0]["displayName"]
            artist_id = str(data["resultsPage"]["results"]["artist"][0]["id"])
            artist_url = data["resultsPage"]["results"]["artist"][0]["uri"]

            logging.info('SK: First result: %s - ID: %s', artist_name, artist_id)

            response = ArtistResponseObject(artist_name,artist_id,artist_url)
            return response
        else:
            logging.info('SK: No artist results found.')
            return None

    def get_events_by_artistID(self, id):
        """
        Queries Songkick 'Artist Event Calendar' search with string 'id' for a list of upcoming events.
        Raises a ValueError if id string is empty.

        If no results are found, returns None.
        If any results are found, using the FIRST result, creates and returns an EventResponseObject.

        Paramaters:
            id: A valid Songkick artist id.
        """

        if not id:
            raise ValueError("Invalid argument. Can't search with empty query.")

        logging.info('SK: Searching for upcoming events for artist ID#%s...', id)

        payload = {'apikey':self.api_key}
        r = requests.get("http://api.songkick.com/api/3.0/artists/"+id+"/calendar.json?", params=payload)
        data = r.json()
        num_results = int(data["resultsPage"]["totalEntries"])

        if num_results !=0:
            logging.info('SK: %d upcoming events found.', num_results)
            list_events = data["resultsPage"]["results"]["event"]

            response = EventResponseObject(num_results,list_events)
            return response
        else:
            logging.info('SK: No events found.')
            return None


class EventResponseObject(object):
    """
    An object containing Songkick information about an Artists event calendar.

    Attributes:
        num_events: The number of upcoming events on an artists calendar.
        list_events: A JSON object containing the list of events.
    """
    def __init__(self, num, list):
        self.num_events = num
        self.list_events = list


class ArtistResponseObject(object):
    """
    An object containing Songkick information about an Artist.

    Attributes:
        name = The artist's name.
        id = The artist's ID on Songkick.
        url = A URL to the artist's page on Songkick.
    """
    def __init__(self, name, id, url):
        self.name = name
        self.id = id
        self.url = url
