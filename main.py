from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtMultimedia import QMediaPlaylist
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor
from os import listdir
from os.path import isfile, join
import sys
import logic


class Worker(QObject):
    info = pyqtSignal(tuple)
    finished = pyqtSignal()

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        self.info.emit(logic.get_metadata(self.path))
        self.finished.emit()


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralwidget = QtWidgets.QWidget(self)
        self.toolBar = QtWidgets.QToolBar(self)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menuSong = QtWidgets.QMenu(self.menubar)
        self.menuInfo = QtWidgets.QMenu(self.menubar)
        self.menuPlaylist = QtWidgets.QMenu(self.menubar)
        self.menuOgolne = QtWidgets.QMenu(self.menubar)
        self.max_vol = QtWidgets.QLabel(self.centralwidget)
        self.prev_button = QtWidgets.QPushButton(self.centralwidget)
        self.min_vol = QtWidgets.QLabel(self.centralwidget)
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.song_name = QtWidgets.QLabel(self.centralwidget)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.volume_slider = QtWidgets.QSlider(self.centralwidget)
        self.timeSlider = QtWidgets.QSlider(self.centralwidget)
        self.playlist_name = QtWidgets.QLabel(self.centralwidget)
        self.current_time = QtWidgets.QLabel(self.centralwidget)
        self.max_time = QtWidgets.QLabel(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.configFile = "confile.txt"
        self.curr_playlist_paths = []
        self.prev_folders = []
        self.saved_playlists = logic.load_saved_songs(self.configFile)
        self.media_setter()
        self.color_mode = 1
        self.ifOne = True

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(812, 349)

        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout.setObjectName("gridLayout")

        self.playlist_name.setAlignment(QtCore.Qt.AlignCenter)
        self.playlist_name.setObjectName("playlist_name")
        self.gridLayout.addWidget(self.playlist_name, 0, 0, 1, 3)

        self.volume_slider.setOrientation(QtCore.Qt.Horizontal)
        self.volume_slider.setObjectName("horizontalSlider")
        self.gridLayout.addWidget(self.volume_slider, 6, 0, 1, 3)
        self.volume_slider.setValue(100)

        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.gridLayout.addWidget(self.timeSlider, 2, 0, 1, 3)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset_button.sizePolicy().hasHeightForWidth())
        self.reset_button.setSizePolicy(sizePolicy)
        self.reset_button.setObjectName("reset_button")
        self.gridLayout.addWidget(self.reset_button, 4, 1, 1, 1)
        self.reset_button.setEnabled(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy)
        self.start_button.setObjectName("start_button")
        self.gridLayout.addWidget(self.start_button, 3, 1, 1, 1)
        self.start_button.setEnabled(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.song_name.sizePolicy().hasHeightForWidth())
        self.song_name.setSizePolicy(sizePolicy)
        self.song_name.setAlignment(QtCore.Qt.AlignCenter)
        self.song_name.setObjectName("song_name")
        self.gridLayout.addWidget(self.song_name, 1, 0, 1, 3)

        self.current_time.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.current_time.setObjectName("current_time")
        self.current_time.setText("0:00")
        self.gridLayout.addWidget(self.current_time, 1, 0, 1, 1)

        self.max_time.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.max_time.setObjectName("max_time")
        self.max_time.setText("0:00")
        self.gridLayout.addWidget(self.max_time, 1, 2, 1, 1)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_button.sizePolicy().hasHeightForWidth())
        self.next_button.setSizePolicy(sizePolicy)
        self.next_button.setObjectName("next_button")
        self.gridLayout.addWidget(self.next_button, 3, 2, 1, 1)
        self.next_button.setEnabled(False)

        self.min_vol.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.min_vol.setObjectName("min_vol")
        self.gridLayout.addWidget(self.min_vol, 7, 0, 1, 1)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prev_button.sizePolicy().hasHeightForWidth())
        self.prev_button.setSizePolicy(sizePolicy)
        self.prev_button.setObjectName("prev_button")
        self.gridLayout.addWidget(self.prev_button, 3, 0, 1, 1)
        self.prev_button.setEnabled(False)

        self.max_vol.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.max_vol.setObjectName("max_vol")
        self.gridLayout.addWidget(self.max_vol, 7, 2, 1, 1)

        self.setCentralWidget(self.centralwidget)

        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 21))
        self.menubar.setObjectName("menubar")
        self.menuSong.setObjectName("menuOpcje")
        self.menuInfo.setObjectName("menuInfo")
        self.menuPlaylist.setObjectName("menuPlaylist")
        self.menuOgolne.setObjectName("menuOgolne")
        self.setMenuBar(self.menubar)

        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi()
        self.connections()
        self.create_menus()
        self.dark_mode()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Mp3 player"))
        self.playlist_name.setText(_translate("MainWindow", "NAZWA PLAYLISTY"))
        self.reset_button.setText(_translate("MainWindow", "Restart"))
        self.start_button.setText(_translate("MainWindow", "start"))
        self.song_name.setText(_translate("MainWindow", "NAZWA PIOSENKI - WYKONAWCA"))
        self.next_button.setText(_translate("MainWindow", "Następna"))
        self.min_vol.setText(_translate("MainWindow", "Min.Vol"))
        self.prev_button.setText(_translate("MainWindow", "Poprzednia"))
        self.max_vol.setText(_translate("MainWindow", "Max. Vol"))
        self.menuSong.setTitle(_translate("MainWindow", "Piosenki"))
        self.menuInfo.setTitle(_translate("MainWindow", "Info"))
        self.menuPlaylist.setTitle(_translate("MainWindow", "Playlist"))
        self.menuOgolne.setTitle(_translate("MainWindow", "Ogolne"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

    def create_menus(self):
        self.menuSong.addAction(self.actionwybierz_piosenke)
        self.menuSong.addAction(self.actiondodaj_folder)
        self.menuSong.addAction(self.actiondodaj_piosenke)
        self.menuSong.addAction(self.actionwybierz_folder)
        self.menuSong.addAction(self.actionlista_piosenek)
        self.menuSong.addAction(self.actionWyszukaj_piosenk)
        self.menuSong.addAction(self.actionhistoria_folderow)

        self.menuPlaylist.addAction(self.actionstworz_playliste)
        self.menuPlaylist.addAction(self.actionzmien_nazwe_playlisty)
        self.menuPlaylist.addAction(self.actiondodaj_piosenke_do_play)
        self.menuPlaylist.addAction(self.actiondodaj_piosenk_do_ulubionych)
        self.menuPlaylist.addAction(self.selectSavedS)

        self.menuInfo.addAction(self.actionpobierz_informacje_piosenek)
        self.menuInfo.addAction(self.actionwy_wietl_tekst_piosenki)
        self.menuInfo.addAction(self.show_information)

        self.menuOgolne.addAction(self.color_change)

        self.menubar.addAction(self.menuSong.menuAction())
        self.menubar.addAction(self.menuPlaylist.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())
        self.menubar.addAction(self.menuOgolne.menuAction())

        self.toolBar.addAction(self.actiondodaj_piosenke)
        self.toolBar.addAction(self.actiondodaj_piosenk_do_ulubionych)
        self.toolBar.addAction(self.randomizePlaylist)

    def connections(self):
        self.actionwybierz_piosenke = QAction("wybierz piosenke", self, triggered=self.select_song)
        self.actiondodaj_piosenke = QAction("dodaj piosenkę", self, triggered=self.add_song)
        self.actionwybierz_folder = QAction("dodaj folder", self, triggered=self.add_folder)
        self.actiondodaj_folder = QAction("wybierz folder", self, triggered=self.select_folder)
        self.actionlista_piosenek = QAction("lista piosenek", self, triggered=self.song_list)
        self.actionstworz_playliste = QAction("Stwórz playliste", self, triggered=self.create_playlist)
        self.actionzmien_nazwe_playlisty = QAction("zmien nazwe playlisty", self, triggered=self.change_playlist_name)
        self.actiondodaj_piosenke_do_play = QAction("dodaj piosenkę do playlisty", self,
                                                    triggered=self.add_song_to_playlist)
        self.actiondodaj_piosenk_do_ulubionych = QAction("dodaj piosenkę do ulubionych", self,
                                                         triggered=self.add_to_fav)
        self.actionpobierz_informacje_piosenek = QAction("pobierz informacje piosenek", self,
                                                         triggered=self.download_info)
        self.selectSavedS = QAction("&Przegladaj zapisane playlisty", self, triggered=self.select_playlist)
        self.actionwy_wietl_tekst_piosenki = QAction("wyświetl tekst piosenki", self, triggered=self.show_song_text)
        self.actionhistoria_folderow = QAction("historia folderow", self, triggered=self.history)
        self.actionWyszukaj_piosenk = QAction("Wyszukaj piosenkę", self, triggered=self.serch_song)
        self.prev_button.clicked.connect(lambda: self.prev())
        self.next_button.clicked.connect(lambda: self.next())
        self.start_button.clicked.connect(lambda: self.start())
        self.reset_button.clicked.connect(lambda: self.reset())
        self.volume_slider.valueChanged.connect(lambda: self.volumeChange())
        self.randomizePlaylist = QAction("graj piosenki losowo", self, triggered=self.random_mode)
        self.show_information = QAction("Wyswietl informacje", self, triggered=self.show_song_info)
        self.color_change = QAction("Zmien kolory", self, triggered=self.dark_mode)

    def dynamicConnections(self):
        self.player.playlist().currentIndexChanged.connect(lambda: self.endOfPlaylist())
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.timeSlider.valueChanged.connect(self.player.setPosition)

    def media_setter(self):
        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(2)
        self.player = QMediaPlayer()

    def setting_player(self):
        self.start_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.player.setPlaylist(self.playlist)
        self.dynamicConnections()
        self.song_name.setText(self.curr_playlist_paths[self.player.playlist().currentIndex()].name)
        self.player.setVolume(self.volume_slider.value())
        self.start_button.setText("start")

    def is_saved(self, path):
        for key in self.saved_playlists.keys():
            for song in self.saved_playlists[key]:
                if song.path == path:
                    return True, song
        return False, None

    def closeEvent(self, event):
        close = QMessageBox()
        close.setWindowTitle("Closing")
        close.setText("Are you sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            try:
                logic.save_playlists(self.configFile, self.saved_playlists)
            except IOError as err:
                self.statusbar.showMessage(err)
            event.accept()
        else:
            event.ignore()

    def update_position(self, position):
        if position >= 0:
            self.current_time.setText(logic.hhmmss(position))

        self.timeSlider.blockSignals(True)
        self.timeSlider.setValue(position)
        self.timeSlider.blockSignals(False)

    def update_duration(self, duration):
        self.timeSlider.setMaximum(duration)
        if duration >= 0:
            self.max_time.setText(logic.hhmmss(duration))

    def volumeChange(self):
        self.player.setVolume(self.volume_slider.value())
        self.statusbar.showMessage("changing volume...")

    def endOfPlaylist(self):
        if self.player.playlist().currentIndex() == -1:
            self.start_button.setText("start")
            self.song_name.setText(self.curr_playlist_paths[0].name)
            self.statusbar.showMessage("playlist ended")
        else:
            self.song_name.setText(self.curr_playlist_paths[self.player.playlist().currentIndex()].name)
        self.statusbar.showMessage("playing next song")

    def dark_mode(self):
        main.setStyle("Fusion")
        palette = QPalette()
        if self.color_mode == 0:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(235, 101, 54))
            palette.setColor(QPalette.Highlight, QColor(235, 101, 54))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            main.setPalette(palette)
            self.color_mode = 1
        elif self.color_mode == 1:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, Qt.white)
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.white)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(66, 155, 248))
            palette.setColor(QPalette.Highlight, QColor(66, 155, 248))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            main.setPalette(palette)
            self.color_mode = 0

    def random_mode(self):
        if len(self.curr_playlist_paths) > 2:
            self.player.playlist().setPlaybackMode(4)
            self.statusbar.showMessage("playing randomly")
        else:
            self.statusbar.showMessage("too small playlist")

    def next(self):
        self.player.playlist().next()
        if self.player.playlist().currentIndex() == -1:
            self.song_name.setText(self.curr_playlist_paths[0].name)
            self.start_button.setText("start")
        else:
            self.song_name.setText(self.curr_playlist_paths[self.player.playlist().currentIndex()].name)
        self.statusbar.showMessage("skipped foreward")

    def prev(self):
        self.player.playlist().previous()

        if self.player.playlist().currentIndex() == -1:
            self.start_button.setText("start")
        else:
            self.song_name.setText(self.curr_playlist_paths[self.player.playlist().currentIndex()].name)
        self.statusbar.showMessage("going back")

    def start(self):
        if self.player.state() == 1:
            self.player.pause()
            self.start_button.setText("start")
            self.statusbar.showMessage("song stopped")
        else:
            self.player.play()
            self.statusbar.showMessage("song started")
            self.start_button.setText("stop")

    def reset(self):
        self.player.stop()
        self.start_button.setText("start")
        self.statusbar.showMessage("song reseted")

    def select_song(self):
        song, _ = QFileDialog.getOpenFileName(self, "Open Song", "", "Sound Files (*.mp3 *.ogg *.wav *.m4a)")
        if song:
            self.curr_playlist_paths = []
            self.media_setter()
            self.select_song_common(song)
        else:
            self.statusbar.showMessage("no song was choosen")

    def add_song(self):
        song, _ = QFileDialog.getOpenFileName(self, "Open Song", "", "Sound Files (*.mp3 *.ogg *.wav *.m4a)")
        if song:
            self.select_song_common(song)
        else:
            self.statusbar.showMessage("no song was choosen")

    def select_song_common(self, song):
        self.playlist_name.setText("NAZWA PLAYLISTY")
        url = QUrl.fromLocalFile(song)

        b, ss = self.is_saved(song)
        if b:
            self.curr_playlist_paths.append(ss)
        else:
            self.curr_playlist_paths.append(logic.Song(song))

        if len(self.curr_playlist_paths) > 1:
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        else:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)

        self.playlist.addMedia(QMediaContent(url))

        self.setting_player()
        self.statusbar.showMessage("song choosen")

    def select_folder(self):
        response, onlyfiles = self.select_folder_popup()

        if response == "no folder":
            return

        self.curr_playlist_paths = []
        self.media_setter()

        self.select_folder_common(onlyfiles, response)

    def add_folder(self):
        response, onlyfiles = self.select_folder_popup()

        if response == "no folder":
            return
        self.select_folder_common(onlyfiles, response)

    def select_folder_popup(self):
        response = QFileDialog.getExistingDirectory(
            self,
            caption='select folder'
        )
        if response:
            onlyfiles = [f for f in listdir(response) if isfile(join(response, f))]
        else:
            self.statusbar.showMessage("no folder was choosen")
            return "no folder", "no folder"
        return response, onlyfiles

    def select_folder_common(self, onlyfiles, response):
        self.playlist_name.setText("NAZWA PLAYLISTY")
        self.add_folder_histoty(response)

        for song in onlyfiles:
            if song.endswith(".mp3") or song.endswith(".ogg") or song.endswith(".wav") or song.endswith(".m4a"):
                b, ss = self.is_saved(f'{response}/{song}')
                if b:
                    self.curr_playlist_paths.append(ss)
                else:
                    self.curr_playlist_paths.append(logic.Song(f'{response}/{song}'))
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(f'{response}/{song}')))

        if len(self.curr_playlist_paths) == 0:
            self.start_button.setEnabled(False)
            self.reset_button.setEnabled(False)
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.song_name.setText("NAZWA PIOSENKI - WYKONAWCA")
            self.curr_playlist_paths = []
            self.media_setter()
            self.start_button.setText("start")
            self.statusbar.showMessage("folder without songs was choosen")
            return

        if len(self.curr_playlist_paths) > 1:
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        else:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)

        self.setting_player()
        self.statusbar.showMessage("folder choosen")

    def create_playlist(self):
        if len(self.curr_playlist_paths) > 0:
            text, ok = QtWidgets.QInputDialog.getText(self, 'Text Input Dialog', 'Enter name of current playlist:')
            if ok:
                if self.playlist_name.text() == "Ulubione" or self.playlist_name.text() == "NAZWA PLAYLISTY":
                    self.statusbar.showMessage(f'can not create playlist with this name')
                if text == '':
                    self.saved_playlists[f'defaoult_name_{len(self.saved_playlists)}'] = self.curr_playlist_paths
                    self.playlist_name.setText(text)
                    self.statusbar.showMessage(f'album defaoult_name_{len(self.saved_playlists)} saved')
                else:
                    self.saved_playlists[text] = self.curr_playlist_paths
                    self.playlist_name.setText(text)
                    self.statusbar.showMessage(f'album {text} saved')
        self.statusbar.showMessage(f'playlist not created')

    def change_playlist_name(self):
        if len(self.curr_playlist_paths) > 0:
            text, ok = QtWidgets.QInputDialog.getText(self, 'Text Input Dialog', 'Enter new name of current playlist:')
            if ok:
                if text == '' or self.playlist_name.text() == "Ulubione" or self.playlist_name.text() == "NAZWA PLAYLISTY":
                    self.statusbar.showMessage(f'cannot change to this name')
                else:
                    if text in self.saved_playlists.keys():
                        templist = []
                        for _ in range(len(self.saved_playlists[self.playlist_name.text()])):
                            templist.append(self.saved_playlists[self.playlist_name.text()].pop())
                        self.saved_playlists[f'{text}_{len(self.saved_playlists)}'] = templist
                        self.playlist_name.setText(f'{text}_{len(self.saved_playlists)}')
                        self.statusbar.showMessage(f'playlist {text}_{len(self.saved_playlists)} saved')
                    else:
                        templist = []
                        for _ in range(len(self.saved_playlists[self.playlist_name.text()])):
                            templist.append(self.saved_playlists[self.playlist_name.text()].pop())
                        self.saved_playlists[f'{text}'] = templist
                        self.playlist_name.setText(text)
                        self.statusbar.showMessage(f'playlist {text} saved')
                    tempdir = {}
                    for key in self.saved_playlists.keys():
                        if not len(self.saved_playlists[key]) == 0:
                            tempdir[key] = self.saved_playlists[key]
                    self.saved_playlists = tempdir
        else:
            self.statusbar.showMessage(f'no playlist to edit')

    def add_to_fav(self):
        if len(self.curr_playlist_paths) > 0:
            if "Ulubione" not in self.saved_playlists.keys():
                self.saved_playlists["Ulubione"] = []
            if "Ulubione" == self.playlist_name.text():
                return
            if self.curr_playlist_paths[self.player.playlist().currentIndex()].path in self.saved_playlists["Ulubione"]:
                return
            self.saved_playlists["Ulubione"].append(self.curr_playlist_paths[self.player.playlist().currentIndex()])
            self.statusbar.showMessage(f'added to favourite')
        else:
            self.statusbar.showMessage(f'no song to add')

    def add_song_to_playlist(self):
        if len(self.curr_playlist_paths) > 0:
            items = []
            for k in self.saved_playlists.keys():
                items.append(k)
            item, ok = QtWidgets.QInputDialog.getItem(self, 'Text Input Dialog', 'chooes saved playlist:', items)
            if ok and item:
                if item not in self.saved_playlists.keys():
                    return
                if item == self.playlist_name.text():
                    return
                if self.curr_playlist_paths[self.player.playlist().currentIndex()].path in self.saved_playlists[item]:
                    return

                self.saved_playlists[item].append(self.curr_playlist_paths[self.player.playlist().currentIndex()])
            self.statusbar.showMessage(f'song added')
        else:
            self.statusbar.showMessage(f'no song to add')

    def select_playlist(self):
        if not len(self.saved_playlists) == 0:
            items = []
            for k in self.saved_playlists.keys():
                items.append(k)
            item, ok = QtWidgets.QInputDialog.getItem(self, 'Text Input Dialog', 'chooes saved playlist:', items)
            if ok and item:
                if item not in self.saved_playlists.keys():
                    return
                self.curr_playlist_paths = self.saved_playlists.get(item)[:]
                if len(self.curr_playlist_paths) == 0:
                    self.prev_button.setEnabled(False)
                    self.next_button.setEnabled(False)
                    self.start_button.setEnabled(False)
                    self.reset_button.setEnabled(False)
                    self.curr_playlist_paths = []
                    self.media_setter()
                    self.start_button.setText("start")
                    return
                if len(self.curr_playlist_paths) > 1:
                    self.prev_button.setEnabled(True)
                    self.next_button.setEnabled(True)
                else:
                    self.prev_button.setEnabled(False)
                    self.next_button.setEnabled(False)

                self.media_setter()
                for song in self.curr_playlist_paths:
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(song.path)))

                self.setting_player()
                self.playlist_name.setText(item)
                self.statusbar.showMessage(f'playlist choosen')
        else:
            self.statusbar.showMessage(f'no saved albums')

    def song_list(self):
        if len(self.curr_playlist_paths) > 0:
            self.menuSong.setEnabled(False)
            self.actionstworz_playliste.setEnabled(False)
            self.actionpobierz_informacje_piosenek.setEnabled(False)
            self.actiondodaj_piosenke.setEnabled(False)
            newWindow = QDialog(self)
            newWindow.setWindowFlag(Qt.FramelessWindowHint)
            newWindow.setWindowTitle("lista piosenek")
            gridLay = QtWidgets.QGridLayout(newWindow)
            list_widget = QtWidgets.QListWidget(newWindow)
            for p in self.curr_playlist_paths:
                list_widget.addItem(p.name)
            list_widget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
            gridLay.addWidget(list_widget)
            save_button = QtWidgets.QPushButton(newWindow)
            save_button.setText("zapisz")
            cancle_button = QtWidgets.QPushButton(newWindow)
            cancle_button.setText("zamknij")
            gridLay.addWidget(save_button)
            gridLay.addWidget(cancle_button)
            save_button.clicked.connect(lambda: self.zamknij(newWindow, list_widget))
            cancle_button.clicked.connect(lambda: self.zamknij(newWindow))
            newWindow.show()

    def zamknij(self, t_window, s_list=None):
        if s_list is None:
            self.menuSong.setEnabled(True)
            self.actionstworz_playliste.setEnabled(True)
            self.actionpobierz_informacje_piosenek.setEnabled(True)
            self.actiondodaj_piosenke.setEnabled(True)
            t_window.close()
            self.statusbar.showMessage(f'order was not changed')
        else:
            newOrder = []
            for i in range(s_list.count()):
                for j in range(len(self.curr_playlist_paths)):
                    if s_list.item(i).text() == self.curr_playlist_paths[j].name:
                        newOrder.append(self.curr_playlist_paths[j])

            self.curr_playlist_paths = newOrder
            self.media_setter()
            for song in self.curr_playlist_paths:
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(song.path)))

            self.setting_player()
            self.song_name.setText(self.curr_playlist_paths[self.player.playlist().currentIndex()].name)
            self.menuSong.setEnabled(True)
            self.actionstworz_playliste.setEnabled(True)
            self.actionpobierz_informacje_piosenek.setEnabled(True)
            self.actiondodaj_piosenke.setEnabled(True)
            self.statusbar.showMessage(f'order changed')

            if self.playlist_name.text() != "NAZWA PLAYLISTY":
                self.saved_playlists[self.playlist_name.text()] = self.curr_playlist_paths[:]

            t_window.close()

    def serch_song(self):
        items = []
        for key in self.saved_playlists.keys():
            for song in self.saved_playlists[key]:
                if song.name not in items:
                    items.append(song.name)
        item, ok = QtWidgets.QInputDialog.getItem(self, 'search for song', 'songs:', items)
        if ok and item:
            for key in self.saved_playlists.keys():
                for song in self.saved_playlists[key]:
                    if song.name == item:
                        self.curr_playlist_paths = []
                        self.media_setter()
                        self.select_song_common(song.path)

    def history(self):
        items = []
        for folder in self.prev_folders:
            items.append(folder[folder.rfind('/'):])
        item, ok = QtWidgets.QInputDialog.getItem(self, 'Text Input Dialog', 'chooes previous folder:', items)
        if ok and item:
            path = None
            for folder in self.prev_folders:
                if folder[folder.rfind('/'):] == item:
                    path = folder
            if path is not None:
                onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
                self.curr_playlist_paths = []
                self.media_setter()
                self.select_folder_common(onlyfiles, path)
            else:
                self.statusbar.showMessage("no such folder in history")

    def add_folder_histoty(self, folder_path):
        if len(self.prev_folders) == 5:
            self.prev_folders.pop(0)
        self.prev_folders.append(folder_path)

    def download_info(self):

        if len(self.curr_playlist_paths) > 0:
            self.statusbar.showMessage("please wait, downloading information...")
            self.ifOne = not self.next_button.isEnabled()
            self.start_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.prev_button.setEnabled(False)
            self.menuSong.setEnabled(False)
            self.menuPlaylist.setEnabled(False)
            self.menuInfo.setEnabled(False)
            self.player.pause()

            self.thread = QThread()
            self.worker = Worker(self.curr_playlist_paths[self.player.playlist().currentIndex()].path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.info.connect(self.save_info)
            self.thread.start()
        else:
            self.statusbar.showMessage("no song choosen")

    def save_info(self, metadata):
        self.curr_playlist_paths[self.player.playlist().currentIndex()].setName(metadata[0])
        self.curr_playlist_paths[self.player.playlist().currentIndex()].setAuthor(metadata[1])
        self.curr_playlist_paths[self.player.playlist().currentIndex()].setAlbum(metadata[2])
        self.curr_playlist_paths[self.player.playlist().currentIndex()].setYear(metadata[3])
        self.save_song_text(metadata[4])
        for key in self.saved_playlists.keys():
            for songIndex in range(len(self.saved_playlists[key])):
                if self.saved_playlists[key][songIndex].path == self.curr_playlist_paths[
                    self.player.playlist().currentIndex()].path:
                    self.saved_playlists[key][songIndex] = self.curr_playlist_paths[
                        self.player.playlist().currentIndex()]
        self.song_name.setText(self.curr_playlist_paths[self.player.playlist().currentIndex()].name)

        self.start_button.setEnabled(True)
        if not self.ifOne:
            self.next_button.setEnabled(True)
            self.prev_button.setEnabled(True)
        self.menuSong.setEnabled(True)
        self.menuPlaylist.setEnabled(True)
        self.menuInfo.setEnabled(True)
        self.player.play()
        self.statusbar.showMessage("downloading succesfull")

    def save_song_text(self, text):
        p = self.curr_playlist_paths[self.player.playlist().currentIndex()].path
        p = p[p.rfind("/") + 1:]
        p += ".txt"
        try:
            f = open(p, 'w', encoding='utf-8')
        except IOError as err:
            self.statusbar.showMessage(str(err))
            return
        for line in text:
            f.write(line)
            f.write("\n")
        f.close()

    def show_song_text(self):
        if len(self.curr_playlist_paths) > 0:
            try:
                p = self.curr_playlist_paths[self.player.playlist().currentIndex()].path
                p = p[p.rfind("/") + 1:]
                p += ".txt"
                f = open(p, 'r', encoding='utf-8')
            except IOError:
                self.statusbar.showMessage("no downloaded lyrics")
                return

            newWindow = QDialog(self)
            newWindow.setWindowTitle("Tekst piosenki")
            newWindow.resize(500, 700)
            gridLay = QtWidgets.QGridLayout(newWindow)
            list_widget = QtWidgets.QListWidget(newWindow)
            for line in f:
                line = line.rstrip()
                if line:
                    list_widget.addItem(line)
            gridLay.addWidget(list_widget)
            newWindow.show()
            f.close()
        else:
            self.statusbar.showMessage("no song choosen")

    def show_song_info(self):
        if len(self.curr_playlist_paths) > 0:
            newWindow = QDialog(self)
            newWindow.setWindowTitle("Informacje")
            newWindow.resize(300, 100)
            gridLay = QtWidgets.QGridLayout(newWindow)
            list_widget = QtWidgets.QListWidget(newWindow)
            list_widget.addItem(
                f'Nazwa piosenki: {self.curr_playlist_paths[self.player.playlist().currentIndex()].name}')
            list_widget.addItem(
                f'Nazwa albumu: {self.curr_playlist_paths[self.player.playlist().currentIndex()].album}')
            list_widget.addItem(f'Rok wydania: {self.curr_playlist_paths[self.player.playlist().currentIndex()].year}')
            list_widget.addItem(f'Autor: {self.curr_playlist_paths[self.player.playlist().currentIndex()].author}')
            gridLay.addWidget(list_widget)
            newWindow.show()
        else:
            self.statusbar.showMessage("no song choosen")


main = QApplication(sys.argv)
window = Ui_MainWindow()
window.setupUi()
window.show()
sys.exit(main.exec_())
