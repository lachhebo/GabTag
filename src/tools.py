import os
from typing import Dict, List

import gi
import musicbrainzngs as mb

from .extension_manager import is_extension_managed
from .selection_handler import SELECTION

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk  # noqa: E402


def remove_extension(filename: str):
    """
    return the filename without the extension
    """
    namelist = filename.split(".")
    return namelist[0:-1]


def reorder_data(music_brainz_data: Dict):
    """
    take a bunch of data from mz and make it in the form { title = , ...}
    """

    file_tags = {
        "title": "",
        "artist": "",
        "genre": "",
        "cover": "",
        "album": "",
        "track": "",
        "year": "",
    }

    if len(music_brainz_data["recording-list"]) >= 1:

        recording_list = music_brainz_data["recording-list"][0]
        artist = recording_list["artist-credit"][0]["artist"]
        file_tags["title"] = recording_list["title"]
        file_tags["artist"] = artist["name"]

        if "disambiguation" in artist:
            file_tags["genre"] = artist["disambiguation"]
        else:
            file_tags["genre"] = ""

        if "release-list" in recording_list:
            for i in range(len(recording_list["release-list"])):
                try:

                    file_tags["cover"] = mb.get_image(
                        mbid=recording_list["release-list"][i]["id"],
                        coverid="front",
                        size=250,
                    )

                    if isinstance(file_tags, bytes):
                        break

                except mb.musicbrainz.ResponseError:
                    file_tags["cover"] = ""

            # album
            release_list = recording_list["release-list"][0]
            track = release_list["medium-list"][0]["track-list"][0]
            file_tags["album"] = release_list["release-group"]["title"]
            file_tags["track"] = track["number"]

            if "date" in release_list:
                file_tags["year"] = release_list["date"].split("-")[0]
            else:
                file_tags["year"] = ""
        else:
            file_tags["album"] = ""
            file_tags["track"] = ""
            file_tags["year"] = ""
            file_tags["cover"] = ""

    return file_tags


def get_extension_image(filename):
    """
    return a mime from a filename
    """
    namelist = filename.split(".")
    return "/image/" + namelist[-1]


def file_size_to_string(path_file):
    return str(round(os.path.getsize(path_file) / 1000000, 1)) + " Mb"


def music_length_to_string(length):
    minutes = str(int(length / 60))
    seconds = str(int(length % 60))
    return minutes + " minutes " + seconds + " seconds"


def add_filters(dialog):
    filter_png = Gtk.FileFilter()
    filter_png.set_name("Png")
    filter_png.add_mime_type("image/png")
    dialog.add_filter(filter_png)

    filter_jpeg = Gtk.FileFilter()
    filter_jpeg.set_name("jpeg")
    filter_jpeg.add_mime_type("image/jpeg")
    dialog.add_filter(filter_jpeg)


def set_label(view_label, multiple_rows, value):
    if multiple_rows == 1:
        view_label.set_text("")
    else:
        view_label.set_text(value)


def set_text_widget_permission(text_widget, multiple_rows, value):
    if multiple_rows == 1:
        text_widget.set_text("")
        text_widget.set_editable(0)
    else:
        text_widget.set_editable(1)
        text_widget.set_text(value)


def get_file_list(directory: str):
    file_list = []
    for (_, _, file_name) in os.walk(directory):
        file_list.extend(file_name)
        break

    result = []
    for name_file in file_list:
        if is_extension_managed(name_file):
            result.append(name_file)

    return result


def is_selection_valid(default_file_names: List) -> bool:
    file_names = get_filenames_from_selection(SELECTION.selection)

    if len(file_names) != len(default_file_names):
        return False

    for name_file, selected_name_file in zip(default_file_names, file_names):
        if name_file != selected_name_file:
            return False

    return True


def get_filenames_from_selection(selection):
    model, list_iter = selection.get_selected_rows()
    name_files = [model[list_iter[i]][0] for i in range(len(list_iter))]
    return name_files
