import database as db
import folder as fd
import os

def select_media():
    print('Type artist or just press Enter')
    artist = input()
    print('Type characters divided by , without Spaces or just press Enter')
    characters = input()
    print('Type tags divided by , without Spaces or just press Enter')
    tags = input()

    if artist == '': artist = None
    if characters == '': characters = None
    if tags == '': tags = None

    names = db.select_media(characters, artist, tags)
    fd.move_in_folder(names)

    print('\nWhen you finish press Enter')
    input()
    fd.move_out_folder(names)

def add_media():
    name = ""
    artist = ""
    characters = ""
    tags = ""

    while name == "":
        print('Type file name below: ')
        name = input()
    
    print('Type artist name below: ')
    artist = input()
    print('Type character(s) name devided by `,` below: ')
    characters = input()
    print('Type tag(s) name devided by `,` below: ')
    tags = input()

    if artist == "":
        artist = None
    if tags == "":
        tags = None
    if characters == "":
        characters = None

    db.add_media(name, characters, artist, tags)

def add_tag():
    print('Type tag below: ')
    db.add_tag(input())

def add_artist():
    print('Type artist name below: ')
    db.add_artist(input())

def add_character():
    print('Type character name below: ')
    db.add_character(input())

def main():
    print('What you want to do: ')
    print("""
    0. Select media
    1. Add media
    2. Add tag
    3. Add artist
    4. Add character
    5. Create database
    6. Delete database
    """)
    print('Type number below')

    answer = input()
    match answer:
        case '0':
            select_media()
        case '1':
            add_media()
        case '2':
            add_tag()
        case '3':
            add_artist()
        case '4':
            add_character()
        case '5':
            db.create_database()
        case '6':
            db.delete_database()
        # case '7':
        #     set_folder()

while True:
    main()
