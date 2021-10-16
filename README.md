# <img width="30" src="data/icons/hicolor/scalable/apps/com.github.lachhebo.Gabtag.svg"/> GabTag [![codecov](https://codecov.io/gh/lachhebo/GabTag/branch/master/graph/badge.svg)](https://codecov.io/gh/lachhebo/GabTag)


## Description :


GabTag is a Linux audio tagging tool written in GTK 3, which makes it very suitable for GTK based desktop users.

It allows users to select several files and modify their tags. It is also possible to let GabTag automatically find tags and lyrics for an audio file using MusicBrainz and lyrics.wikia database.


<a href='https://flathub.org/apps/details/com.github.lachhebo.Gabtag'><img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/></a>



## Screenshots:


<img height="350" src="https://raw.githubusercontent.com/lachhebo/GabTag/screenshots/Gabtag_v13_2.png" />


## Features :

- [x] Add, modify or delete basic tags (title, album, artist, genre)
- [x] other strings tags and labels
- [x] Cover tag
- [x] Modify several file at the same time.
- [x] MP3  File handled
- [x] bold font on modified tags and files
- [x] Automatic completion of tags (from online data)

## Contributing

To setup development environment on arch based distro:

    make setupenv

To run test:

    make tests

To install:

    make install

to run:

    make run 