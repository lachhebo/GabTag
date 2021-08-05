from src.tools import reorder_data


def test_reorder_data_is_working_with_musicbrainz_data():
    # given

    music_brainz_data = {
        "recording-list": [
            {
                "id": "944c97bc-5341-4834-acb4-73ac24f1602e",
                "ext:score": "100",
                "title": "Bunker Sweet Bunker",
                "length": "175626",
                "artist-credit": [
                    {
                        "name": "Les Malpolis",
                        "artist": {
                            "id": "e32f569d-bcd8-4c29-95a1-b13bff72f9d5",
                            "name": "Les Malpolis",
                            "sort-name": "Malpolis, Les",
                        },
                    }
                ],
                "release-list": [
                    {
                        "id": "577f349b-528e-4366-b26e-ab583af99a49",
                        "title": "Les Malpolis élargissent leur cible",
                        "status": "Official",
                        "release-group": {
                            "id": "faa1080b-0878-391e-bfef-db18b6e5f3ed",
                            "type": "Album",
                            "title": "Les Malpolis élargissent leur cible",
                            "primary-type": "Album",
                        },
                        "date": "2001",
                        "country": "FR",
                        "release-event-list": [
                            {
                                "date": "2001",
                                "area": {
                                    "id": "08310658-51eb-3801-80de-5a0739207115",
                                    "name": "France",
                                    "sort-name": "France",
                                    "iso-3166-1-code-list": ["FR"],
                                },
                            }
                        ],
                        "medium-list": [
                            {
                                "position": "1",
                                "format": "CD",
                                "track-list": [
                                    {
                                        "id": "d4f9c6d8-f616-3434-a9e3-7eab00abb2b6",
                                        "number": "7",
                                        "title": "Bunker Sweet Bunker",
                                        "length": "175626",
                                        "track_or_recording_length": "175626",
                                    }
                                ],
                                "track-count": 17,
                            }
                        ],
                        "medium-track-count": 17,
                        "medium-count": 1,
                    }
                ],
                "artist-credit-phrase": "Les Malpolis",
            }
        ],
        "recording-count": 784,
    }

    # when
    output = reorder_data(music_brainz_data)

    # then
    assert output == {
        "title": 'Bunker Sweet Bunker',
        "artist": "Les Malpolis",
        "genre":"",
        "cover":'',
        "album": 'Les Malpolis élargissent leur cible',
        "track":"7",
        "year":"2001",
    }
