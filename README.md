# Advance tv & movie renamer

## Description

Free and easy to use advance file renamer built with Python. Select TV or Movie & subtitle files and rename and/or move them by specifying a new simple to use format!

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
2. Add format
3. Rename & move file

#### currently supported format types:

```
#title# -> Game of thrones
#year# -> 2011
#pSeason# -> 01
#season# -> 1
#pEpisode# -> 01
#episode# -> 1
#episodeTitle# -> Winter is coming
```

#### Examples:

```
#episodeTitle# - E#pEpisode#S#pSeason# -> Pilot S01E01
```

```
#title# (#year#) -> V for Vandetta (2005)
```

## Future improvements

-   UI rework
-   Click to run
-   Better error handling
-   Other advance features
-   Linux support
-   MacOs support
-   <s>Option to rename directories</s>
-   <s>Bigger selection of format types</s>
-   <s>Move files when renaming by specifying new directory</s>

## Notice
At the moment this product only runs on windows platforms. The support for both Linux and MacOs will be added in the future.

## Credit
Nik Vogrinec - [Github](https://github.com/nikvogri)
