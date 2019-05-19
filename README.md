# <img width="30" src="data/icons/hicolor/scalable/apps/com.lachhebo.Gabtag.svg"/> Marker GabTag [![Build Status](https://travis-ci.com/lachhebo/GabTag.svg?branch=master)](https://travis-ci.com/lachhebo/GabTag) 


## Description :

GabTag is a GTK software written in Python, it allows user to add or modify tags on audio files.
It uses Mutagen to handle tags. I hope to make it available on Flathub as soon as possible.

## Features :

- [x] Add, modify or delete basic tags (title, album, artist, genre)
- [x] other strings tags and labels
- [x] Cover tag
- [x] Modify several file at the same time.
- [x] MP3  File handled
- [ ] Flac File handled
- [ ] bold font on modified tags and files
- [ ] Automatic completion of tags (from web data)
- [ ] Multi-folder modification


## Screenshots:

![ScreenShot](https://raw.githubusercontent.com/lachhebo/GabTag/screenshots/Image3.png)


## Contributions :

GabtTag is written to be as easily maintainable and extensible as possible.

If you want to contribute, there is several thing you can do :

- Add a new Python file to handle a new extension (like flac) and add the new classe in the moteur.py file; you can take as an example the MP3Handler.
- Design a improved icon 
- Improve the layout of the app (window.ui file)
- Add unitary tests (in tests/)
- Work on more advanced features like Automatic tagging (using web)


## Installation :

- clone this repository

## Support/Donation :

[<img height="30" src="https://raw.githubusercontent.com/lachhebo/GabTag/screenshots/donate.png" alt="PayPal"/>](https://www.paypal.me/lachhebo)
