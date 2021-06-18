# Advance tv & movie renamer

## Description

Free and easy to use advance file renamer built with Python. Select TV or Movie & subtitle files and rename and/or move them by specifying a new format!

## Packages

-   tkinter
-   json
-   pathlib
-   os
-   requests
-   parse-torrent-file
-   python-dotenv

## Installation & usage

### Installation

1. To use the application first add your TMDB key to .env in /src directory
2. Run using main.py using py command

### Usage

1. Select tv show / movie & subtitle file
2. Add \*format
3. Rename by clicking the rename button

#### currently supported format types:

```
#title# -> Game of thrones
#year# -> 2011
#season -> 01
#episode# -> 01
#episodeTitle# -> Winter is coming
```

#### Examples:

```
#episodeTitle# - E#episode#S#season# -> Pilot S01E01
```

```
#title# #year# -> V for Vandetta 2005
```

## Future improvements

-   Option to rename directories
-   Bigger selection of format types
-   Move files when renaming by specifying new directory
-   Click to run
-   Better error handling
-   Other advance features

## Credit
Nik Vogrinec - [Github](https://github.com/nikvogri)
