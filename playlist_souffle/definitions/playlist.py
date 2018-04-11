"""Module for defining the Playlist namedtuple."""

from collections import namedtuple

Playlist = namedtuple('Playlist', 'user_id name tracks description')
