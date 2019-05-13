# GabTags [![Build Status](https://travis-ci.com/lachhebo/GabTags.svg?branch=master)](https://travis-ci.com/lachhebo/GabTags) 


## Description :

GabTags is a GTK software written in Python, it allows user to add or modify tags on audio files.

It uses Mutagen to handle tags. I hope to make it available on Flathub as soon as possible.

## Features :

- [x] Add, modify or delete basic tags (title, album, artist, genre)
- [ ] other strings tags (less important)
- [x] Continuous integration
- [x] Modify several file at the same time.
- [x] MP3 file handled
- [ ] Flac File handled
- [x] Cover tag
- [ ] About window
- [ ] Multi-folder modification



## Screenshots:

![ScreenShot](https://raw.githubusercontent.com/lachhebo/GabTags/screenshots/Image1.png)


## Development Instruction:

GabtTags is written to be as easily maintainable and extensible as possible.

### Contributions :

If you want to contribute, you can add a extension Handler :

- you can just add a new Python file to handle a new extension (like .mp3); you can take as an example the MP3Handler.
- Then add your handler in the moteur.py file


### Installation :

clone this repository

## Acknowledgments :


Ismaël Lachheb :  [https://paypal.me/lachhebo?locale.x=fr_FR](https://paypal.me/lachhebo?locale.x=fr_FR)

