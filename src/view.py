import io
import math
import gi
from threading import RLock
from PIL import Image
from . import gabtag_logger
from gi.repository import GdkPixbuf, GLib
gi.require_version('Gtk', '3.0')


verrou_tags = RLock()
verrou_mbz = RLock()
verrou_lyrics = RLock()


class View:
    class __View:

        def __init__(self, tree_view, title, album, artist, genre, cover,
                     track, year, length, size, mbz, lyrics):
            """
            Here, we initialise the widget we are going to use in the future.
            """

            self.tree_view = tree_view
            self.title = title
            self.album = album
            self.artist = artist
            self.genre = genre
            self.cover = cover
            self.track = track
            self.year = year
            self.length = length
            self.size = size

            # size of the cover
            self.cover_width = 250
            self.cover_height = 250
            self.last_cover = ''

            if mbz is not None:
                self.title_mbz = mbz[0]
                self.album_mbz = mbz[1]
                self.artist_mbz = mbz[2]
                self.genre_mbz = mbz[3]
                self.cover_mbz = mbz[4]
                self.track_mbz = mbz[5]
                self.year_mbz = mbz[6]

            self.lyrics = lyrics

            if self.lyrics is not None:
                self.lyrics.set_justification(2)  # CENTER
                self.lyrics.set_wrap_mode(2)  # Cut between Word
                self.lyrics_buf = self.lyrics.get_buffer()

        def show_lyrics(self, lyrics_scrapped):
            with verrou_lyrics:
                self.lyrics_buf.set_text(lyrics_scrapped)

        def show_mbz(self, data_scrapped):
            with verrou_mbz:

                # We show the tag currently in tag_dico
                self.title_mbz.set_text(data_scrapped['title'])
                self.track_mbz.set_text(data_scrapped['track'])
                self.genre_mbz.set_text(data_scrapped['genre'])
                self.album_mbz.set_text(data_scrapped['album'])
                self.artist_mbz.set_text(data_scrapped['artist'])
                self.year_mbz.set_text(data_scrapped['year'])

                if data_scrapped['cover'] != '':
                    with Image.open(io.BytesIO(data_scrapped['cover'])) as img:

                        try:
                            glib_bytes = GLib.Bytes.new(img.tobytes())
                            pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(
                                                glib_bytes,
                                                GdkPixbuf.Colorspace.RGB,
                                                False,
                                                8,
                                                img.width,
                                                img.height,
                                                len(img.getbands())*img.width)

                            pixbuf = pixbuf.scale_simple(
                                250, 250, GdkPixbuf.InterpType.BILINEAR)

                            self.cover_mbz.set_from_pixbuf(pixbuf)
                        except TypeError as error_message:
                            self.cover_mbz.set_from_icon_name(
                                'gtk-missing-image', 6)
                            gabtag_logger.error(error_message)
                else:
                    self.cover_mbz.set_from_icon_name('gtk-missing-image', 6)

        def erase(self):
            """
            We erase value written in the GtkEntry of each of those tags
            """
            self.genre.set_text('')
            self.album.set_text('')
            self.title.set_text('')
            self.artist.set_text('')
            self.year.set_text('')
            self.track.set_text('')
            self.cover.set_from_icon_name('gtk-missing-image', 6)
            self.last_cover = ''
            self.show_lyrics('')
            self.show_mbz({'title': '', 'track': '', 'album': '',
                           'genre': '', 'artist': '', 'cover': '', 'year': ''})

        def set_title_permission(self, multiple_rows, title):
            if multiple_rows == 1:
                self.title.set_text('')
                self.title.set_editable(0)
            else:
                self.title.set_editable(1)
                self.title.set_text(title)

        def set_track_permission(self, multiple_rows, track):
            if multiple_rows == 1:
                self.track.set_text('')
                self.track.set_editable(0)
            else:
                self.track.set_editable(1)
                self.track.set_text(track)

        def set_size(self, multiple_rows, size):
            if multiple_rows == 1:
                self.size.set_text('')
            else:
                self.size.set_text(size)

        def set_length(self, multiple_rows, length):
            if multiple_rows == 1:
                self.length.set_text('')
            else:
                self.length.set_text(length)

        def show_cover_from_bytes(self, bytes_file):
            with Image.open(io.BytesIO(bytes_file)) as img:
                glib_bytes = GLib.Bytes.new(img.tobytes())

                width = img.width  # The best fix i could find for the moment
                height = img.height
                if glib_bytes.get_size() < width * height * 3:
                    width = math.sqrt(glib_bytes.get_size() / 3)
                    height = math.sqrt(glib_bytes.get_size() / 3)

                pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(
                                            glib_bytes,
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            width,
                                            height,
                                            len(img.getbands()) * img.width)

                pixbuf = pixbuf.scale_simple(self.cover_width,
                                             self.cover_height,
                                             GdkPixbuf.InterpType.BILINEAR)

                self.cover.set_from_pixbuf(pixbuf)

        def show_cover_from_file(self, name_file):
            with Image.open(name_file) as img:
                glib_bytes = GLib.Bytes.new(img.tobytes())

                pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(
                                            glib_bytes,
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            img.width,
                                            img.height,
                                            len(img.getbands()) * img.width)

                pixbuf = pixbuf.scale_simple(self.cover_width,
                                             self.cover_height,
                                             GdkPixbuf.InterpType.BILINEAR)

                self.cover.set_from_pixbuf(pixbuf)

        def show_tags(self, tags_dict, multiple_rows):
            with verrou_tags:
                # We show those tags uniquely if there is only one row selected
                # TODO is it really useful ? I don't think so
                self.set_title_permission(
                    multiple_rows, tags_dict['title']['value'])
                self.set_track_permission(
                    multiple_rows, tags_dict['track']['value'])

                # TODO show size and length for the concatenation of songs
                # Same thing for the labels
                self.set_size(multiple_rows, tags_dict['size']['value'])
                self.set_length(multiple_rows, tags_dict['length']['value'])

                # We show the tag currently in tags_dict
                self.genre.set_text(tags_dict['genre']['value'])
                self.album.set_text(tags_dict['album']['value'])
                self.artist.set_text(tags_dict['artist']['value'])
                self.year.set_text(tags_dict['year']['value'])
                # TODO : print tags lyrics in case of missing internet lyrics

                # A test to handle if there is a cover
                if tags_dict['cover']['value'] != '':
                    if tags_dict['cover']['value'] != self.last_cover:
                        # A test to detect bytes file
                        if type(tags_dict['cover']['value']) == bytes:
                            self.show_cover_from_bytes(
                                tags_dict['cover']['value'])
                            self.last_cover = tags_dict['cover']['value']
                        else:
                            self.show_cover_from_file(
                                tags_dict['cover']['value'])
                            self.last_cover = tags_dict['cover']['value']
                    else:
                        pass
                else:

                    self.cover.set_from_icon_name('gtk-missing-image', 6)
                    self.last_cover = ''

    __instance = None

    def __init__(self,
                 tree_view, title, album, artist, genre, cover, track,
                 year, length, size, mbz, lyrics):
        """ Virtually private constructor. """
        if View.__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            View.__instance = View.__View(tree_view, title, album, artist,
                                          genre, cover, track, year, length,
                                          size, mbz, lyrics)

    @staticmethod
    def get_instance():
        """ Static access method. """
        if View.__instance is None:
            View(None, None, None, None, None, None,
                 None, None, None, None, None, None)
        return View.__instance
