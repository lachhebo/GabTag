import musicbrainzngs as mb


def remove_extension(filename):
    """
    return the filename without the extension
    """
    namelist = filename.split('.')
    return namelist[0:-1]


def reorder_data(music_brainz_data):
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
        "year": ""}

    if len(music_brainz_data['recording-list']) >= 1:
        file_tags["title"] = music_brainz_data['recording-list'][0]['title']
        file_tags["artist"] = music_brainz_data['recording-list'][0]['artist-credit'][0]["artist"]["name"]

        if 'disambiguation' in music_brainz_data['recording-list'][0]['artist-credit'][0]["artist"]:
            file_tags["genre"] = music_brainz_data['recording-list'][0]['artist-credit'][0]["artist"][
                "disambiguation"]
        else:
            file_tags["genre"] = ""

        if 'release-list' in music_brainz_data['recording-list'][0]:
            for i in range(len(music_brainz_data['recording-list'][0]["release-list"])):
                try:

                    file_tags["cover"] = mb.get_image(
                        mbid=music_brainz_data['recording-list'][0]["release-list"][i]["id"], coverid="front", size=250)

                    if type(file_tags) == bytes:
                        break
                except:
                    file_tags["cover"] = ""

            # album
            file_tags["album"] = music_brainz_data['recording-list'][0]['release-list'][0]["release-group"][
                "title"]
            file_tags["track"] = \
                music_brainz_data['recording-list'][0]['release-list'][0]["medium-list"][0]['track-list'][0][
                    "number"]
            if 'date' in music_brainz_data['recording-list'][0]['release-list'][0]:
                file_tags["year"] = \
                    music_brainz_data['recording-list'][0]['release-list'][0]["date"].split("-")[
                        0]
            else:
                file_tags["year"] = ""
        else:
            file_tags["album"] = ""
            file_tags["track"] = ""
            file_tags["year"] = ""
            file_tags["cover"] = ""

    return file_tags


def get_file_extension(filename):
    """
    return the file extension.
    """
    namelist = filename.split('.')
    return namelist[-1]


def get_extension_mime(filename):
    """
    return the type of the file (jpeg or png)
    """
    namelist = filename.split('/')
    return namelist[-1]


def get_extension_image(filename):
    """
    return a mime from a filename
    """
    namelist = filename.split('.')
    return '/image/' + namelist[-1]


def is_selection_equal(selection, length_selection_2, file_list_selection2):
    model, list_iteration = selection.get_selected_rows()

    if len(list_iteration) == length_selection_2:
        for i in range(len(list_iteration)):
            name_file = model[list_iteration[i]][0]
            if name_file not in file_list_selection2:
                return False
    else:
        return False

    return True
