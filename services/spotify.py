from spotipy import Spotify
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


class SpotipyClient(Spotify):
    '''
    Description: Interface to spotipy lib
    '''

    def __init__(self, username=None):
        self.username = username
        # token = self._get_session_token()
        # self.client = Spotify(auth=token)
        client_credentials_manager = SpotifyClientCredentials()
        self.client = Spotify(
            client_credentials_manager=client_credentials_manager
        )
        #self.client = Spotify()

    def _get_session_token(self):
        """
        Get one time session token
        """
        token = util.prompt_for_user_token(self.username)
        if token:
            return token
        else:
            print("Can't get token for", self.username)

    def get_user_id(self):
        """
        Get user id of account
        """
        pass

    def get_top_artists(self, n: int = 5):
        """
        Get n top artists of users profile
        """
        pass

    def get_user_playlists(self):
        playlists = self.client.user_playlists(self.username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == self.username:
                print()
                print(playlist['name'])
                print('  total tracks', playlist['tracks']['total'])
                results = self.client.user_playlist(
                    self.username,
                    playlist['id'],
                    fields="tracks,next"
                )
                tracks = results['tracks']
                self._show_tracks(tracks)
                while tracks['next']:
                    tracks = self.client.next(tracks)
                    self._show_tracks(tracks)

    def _show_tracks(self, tracks):
        for i, item in enumerate(tracks['items']):
            track = item['track']
            if track:
                print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))
