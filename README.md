# GabTags [![Build Status](https://travis-ci.com/lachhebo/GabTag.svg?branch=master)](https://travis-ci.com/lachhebo/GabTag) 


## Description :

GabTag is a GTK software written in Python, it allows user to add or modify tags on audio files.
It uses Mutagen to handle tags. I hope to make it available on Flathub as soon as possible.

## Features :

- [x] Add, modify or delete basic tags (title, album, artist, genre)
- [x] other strings tags and labels
- [x] Continuous integration
- [x] Modify several file at the same time.
- [x] MP3  File handled
- [ ] Flac File handled
- [x] Cover tag
- [x] About window
- [ ] Automatic completion of tags (from web data)
- [ ] Multi-folder modification
- [x] Icon, AppData file
- [ ] Flathub repository 



## Screenshots:

![ScreenShot](https://raw.githubusercontent.com/lachhebo/GabTags/screenshots/Image2.png)


## Contributions :

GabtTag is written to be as easily maintainable and extensible as possible.

If you want to contribute, there is several thing you can do :

- Add a new Python file to handle a new extension (like .mp3) and add the new classe in the moteur.py file; you can take as an example the MP3Handler.
- Design a improved icon 
- Improve the layout of the app (window.ui file)
- Add unitary tests (in tests/)
- Multi-folder tree in the left panel 
- Work on more advanced features like Automatic tagging (using web)


## Installation :

- clone this repository

## Support/Donation :

Ismaël Lachheb :  [https://paypal.me/lachhebo](https://paypal.me/lachhebo)

