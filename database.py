from contextlib import closing
import sqlite3

DB_PATH = "app.db"

def create_database():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(300) NOT NULL
                );
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(300) NOT NULL
                );            
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(300) NOT NULL
                );                         
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path VARCHAR(300) NOT NULL,
                artist_id INTEGER REFERENCES artists(id)
                );                            
            """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS tags_media (
                tag_id INTEGER REFERENCES tags(id),
                media_id INTEGER REFERENCES media(id),
                PRIMARY KEY (tag_id, media_id)
                );                                  
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS char_media (
                char_id INTEGER REFERENCES characters(id),
                media_id INTEGER REFERENCES media(id),
                PRIMARY KEY (char_id, media_id)
                );
            """)

def _add_meta(mtype:str, data:str, conn: sqlite3.Connection = None):
    data = data.strip().lower().replace(" ", "_")
    connFlag = False
    if conn == None:
        conn = sqlite3.connect(DB_PATH)
        connFlag = True

    with conn:
        cur = conn.execute(
            f"SELECT id FROM {mtype} WHERE name = ?", 
            (data,),
        )

        if cur.fetchone() is not None:
            print(f"{mtype} уже добавлен в базу")
            return

        conn.execute(
            f"INSERT INTO {mtype} (name) VALUES (?)",
            (data,),
        )

    if connFlag == True:
        conn.close()

def _get_meta_ids(mtype:str, items:list, conn: sqlite3.Connection = None) -> list:
    meta_ids = []
    
    connFlag = False
    if conn == None:
        conn = sqlite3.connect(DB_PATH)
        connFlag = True

    with conn:    
        for item in items:
            row = conn.execute(
                f"SELECT id FROM {mtype} WHERE name = ?",
                (item,),
            ).fetchone()
            if row is None:
                _add_meta(mtype, item, conn)
                _row = conn.execute(
                    f"SELECT id FROM {mtype} WHERE name = ?",
                    (item,),
                ).fetchone()
                meta_ids.append(_row[0])
            else:
                meta_ids.append(row[0])

    if connFlag == True:
        conn.close()

    return(meta_ids)

def _get_meta_id(mtype:str, item:str, conn: sqlite3.Connection = None) -> int:
    connFlag = False
    if conn == None:
        conn = sqlite3.connect(DB_PATH)
        connFlag = True

    with conn:    
        row = conn.execute(
            f"SELECT id FROM {mtype} WHERE name = ?",
            (item,),
        ).fetchone()
        if row is None:
            _add_meta(mtype, item, conn)
            _row = conn.execute(
                f"SELECT id FROM {mtype} WHERE name = ?",
                (item,),
            ).fetchone()
            meta_id = _row[0]
        else:
            meta_id = row[0]

    if connFlag == True:
        conn.close()

    return(meta_id)
    
def add_character(char: str, conn: sqlite3.Connection = None):
    _add_meta("characters", char, conn)

def add_tag(tag: str, conn: sqlite3.Connection = None):
    _add_meta("tags", tag, conn)
        
def add_artist(artist: str, conn: sqlite3.Connection = None):
    _add_meta("artists", artist, conn)

def add_media(path:str, chars:str = "", artist: str = "", tags:str = ""):
    chars = chars.strip().lower().replace(" ", "_").split(",")
    artist = artist.strip().lower().replace(" ", "_")
    tags = tags.strip().lower().replace(" ", "_").split(",")

    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            #проверка добавлено ли медиа уже
            cur = conn.execute(
                "SELECT id FROM media WHERE path = ?",
                (path,),
            )
            if cur.fetchone() is not None:
                print("media с таким path уже добавлен в базу")
                return()

            #получение списка id
            char_ids = _get_meta_ids("characters", chars, conn)
            artist_id = _get_meta_id("artists", artist, conn)
            tag_ids = _get_meta_ids("tags", tags, conn)

            conn.execute(
                "INSERT INTO media (path, artist_id) VALUES (?, ?)",
                (path, artist_id),
            )

            media_id = conn.execute(
                "SELECT id FROM media WHERE path = ?",
                (path, ),
            ).fetchone()[0]

            for char_id in char_ids:
                conn.execute(
                    "INSERT OR IGNORE INTO char_media (char_id, media_id) VALUES (?, ?)",
                    (char_id, media_id),
                )

            for tag_id in tag_ids:
                conn.execute(
                    "INSERT OR IGNORE INTO tags_media(tag_id, media_id) VALUES (?, ?)",
                    (tag_id, media_id),
                )
