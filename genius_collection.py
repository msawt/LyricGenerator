import lyricsgenius
import os
#pip3 install python-dotenv
from dotenv import load_dotenv
load_dotenv()

import json
import pandas as pd

token = os.getenv('GENIUS_API_KEY')
genius = lyricsgenius.Genius(token)

def create_lyrics_json_file(artist_name):
    artist = genius.search_artist(artist_name, sort="title")
    artist.save_lyrics()

def parse_json_to_csv(file_name):
    csv_file = file_name.replace(".json", ".csv")
    json_file = file_name

    with open(json_file) as file:
        data = json.load(file)
    
    lyrics = []

    for song in data["songs"]:
        lyric = song["lyrics"].replace('\n', ' ')

        lyrics.append(lyric)

    print("Saving lyrics to csv file...")

    lyrics = pd.DataFrame(lyrics)
    lyrics.to_csv(csv_file, index=False)

    print("Done.")

if __name__ == "__main__":
    #type the artists you want to extract
    artists = ["PREP", "HONNE"]

    genius.skip_non_songs = True
    genius.remove_section_headers = True
    #will have to adjust this so we do not have duplicate songs
    genius.excluded_terms = ["(Remix)", "(london session)", "(dream edit)", "(Late Night Version)", "(Aminé Remix)", 
    "(The Lonely Players Club)", "(Livingston Session)", "(Duet Version)", "(Live)", "(Session)", "(Demo)", "(A Cappella)", "(Leak)", "(Version)", "(Remastered)", "(mix)"]

    for artist in artists:
        print("Working on {0}...".format(artist))
        create_lyrics_json_file(artist)
        print("Done.")

    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".json"):
            print("Parsing {0}...".format(filename))
            parse_json_to_csv(filename)
            print("Done.")