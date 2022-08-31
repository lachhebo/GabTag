<img align="left" style="vertical-align: middle" src="data/icons/hicolor/scalable/apps/com.github.lachhebo.Gabtag.svg"/>

# GabTag

[![codecov](https://codecov.io/gh/lachhebo/GabTag/branch/master/graph/badge.svg)](https://codecov.io/gh/lachhebo/GabTag)

GabTag is a Linux audio tagging tool written in GTK 4 and Adwaita, which makes it very suitable for GTK based desktop users.

It allows users to select several files and modify their tags. It is also possible to let GabTag automatically find tags for an audio file using MusicBrainz.

<p align="center"><img src="https://raw.githubusercontent.com/lachhebo/GabTag/screenshots/Gabtag_v13_2.png#gh-light-mode-only"/></p>
<p align="center"><img src="https://raw.githubusercontent.com/lachhebo/GabTag/screenshots/Gabtag_v13_1.png#gh-dark-mode-only"/></p>


<p align="center"<a href='https://flathub.org/apps/details/com.github.lachhebo.Gabtag'><img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/></a></p>

## Features :

- Add, modify or delete basic tags (title, album, artist, genre)
- other strings tags and labels
- Cover tag
- Modify several file at the same time.
- MP3  File handled
- bold font on modified tags and files
- Automatic completion of tags (from online data)

## Contributing

To setup development environment on arch based distro:

    make setupenv

To run test:

    make tests

To install:

    make install

to run:

    make run 
