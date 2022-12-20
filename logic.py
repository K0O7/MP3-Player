class Song:
    def __init__(self, path, name='', author="def", album="def", year="def"):
        self.path = path
        if name == '':
            self.name = path[path.rfind('/') + 1:]
        else:
            self.name = name
        self.author = author
        self.album = album
        self.year = year

    def setName(self, name):
        self.name = name

    def setAuthor(self, author):
        self.author = author

    def setAlbum(self, album):
        self.album = album

    def setYear(self, year):
        self.year = year

    def __str__(self):
        return f'{self.path}\n{self.name}\n{self.author}\n{self.album}\n{self.year}\n'


def load_saved_songs(conFile):
    dirOfPlaylists = {}
    infoCounter = 0
    try:
        f = open(conFile, 'r', encoding='utf-8')
    except IOError as err:
        f = open(conFile, 'w', encoding='utf-8')
        f.close()
        return {}
    temp_key = ''
    p = ''
    n = ''
    a = ''
    al = ''
    for l in f:
        if l.endswith("\n"):
            l = l[:len(l) - 1]
        if l[0] == '|':
            l = l[1:]
            if l not in dirOfPlaylists.keys():
                dirOfPlaylists[l] = []
            temp_key = l
        elif infoCounter == 0:
            p = l
            infoCounter += 1
        elif infoCounter == 1:
            n = l
            infoCounter += 1
        elif infoCounter == 2:
            a = l
            infoCounter += 1
        elif infoCounter == 3:
            al = l
            infoCounter += 1
        elif infoCounter == 4:
            infoCounter = 0
            dirOfPlaylists[temp_key].append(Song(p, n, a, al, l))
    return dirOfPlaylists


def save_playlists(saveFile, playlists):
    try:
        f = open(saveFile, 'w', encoding='utf-8')
    except IOError as err:
        return err
    for key in playlists.keys():
        f.write(f'|{key}')
        f.write('\n')
        for song in playlists[key]:
            if song not in playlists.keys():
                f.write(str(song))
    f.close()


def hhmmss(ms):
    # s = 1000
    # m = 60000
    # h = 360000
    s = round(ms / 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))


def get_metadata(song_path):
    from ShazamAPI import Shazam

    Title = 'def'
    author = 'def'
    album = 'def'
    year = 'def'
    text = 'no text found'

    mp3_file_content_to_recognize = open(song_path, 'rb').read()
    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()
    num, metadata = next(recognize_generator)
    for key in metadata.keys():
        if key == "track":
            for k in metadata[key].keys():
                if k == "title":
                    Title = metadata[key][k]
                if k == "sections":
                    for type in metadata[key][k]:
                        if "LYRICS" == type["type"]:
                            if "text" in type.keys():
                                text = type["text"]
                                # print(type["text"])

                        if "SONG" == type["type"]:
                            for dict in type["metadata"]:
                                if "title" in dict.keys():
                                    if dict["title"] == "Album":
                                        album = dict["text"]
                                        # print(album)
                                    if dict["title"] == "Released":
                                        year = dict["text"]
                                        # print(year)

                        if "ARTIST" == type["type"]:
                            if "name" in type.keys():
                                author = type["name"]
                                # print(type["name"])
    return Title, author, album, year, text
