import database as db

def select_media():
    print('By what you want select')
    print("""
        1. Artist
        2. Character
        3. Tag
        """)
    
    answer = input()
    match answer:
        case '1':
            print('Type artist name below')
            artist = input()
            paths = db.select_media(artist=artist)
        case '2':
            print('Type character name below')
            character = input()
            paths = db.select_media(character=character)
        case '3':
            print('Type tag below')
            tag = input()
            paths = db.select_media(tag=tag)

def add_media():
    path = ""
    artist = ""
    characters = ""
    tags = ""

    while path == "":
        print('Type path below: ')
        path = input()
    else:
        print('Path is empty, type again')
        # добавить проверку на правильность пути
    
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

    db.add_media(path, characters, artist, tags)

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

while True:
    main()
