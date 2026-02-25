import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel
from PyQt6.QtCore import Qt, QUrl, pyqtSignal, QTime
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

class AudioPlayerWidget(QWidget):
    def __init__(self, media_path: str, parent=None):
        super().__init__(parent)
        self.media_path = media_path
        
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        
        # Load Media safely
        if self.media_path and isinstance(self.media_path, str):
            if os.path.exists(self.media_path):
                self.player.setSource(QUrl.fromLocalFile(os.path.abspath(self.media_path)))
            
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Style
        self.setStyleSheet("""
            QWidget {
                background-color: #EDF2F7;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #4C51BF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #434190;
            }
            QLabel {
                color: #2D3748;
                font-size: 13px;
                font-family: monospace;
                font-weight: bold;
            }
            QSlider::groove:horizontal {
                border: 1px solid #CBD5E0;
                height: 6px;
                background: #E2E8F0;
                margin: 2px 0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4A5568;
                border: 1px solid #2D3748;
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #4C51BF;
                border: 1px solid #434190;
                height: 6px;
                border-radius: 3px;
            }
        """)
        
        self.btn_play_pause = QPushButton("▶ Play")
        self.btn_play_pause.setFixedWidth(80)
        layout.addWidget(self.btn_play_pause)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)
        layout.addWidget(self.slider)
        
        self.lbl_time = QLabel("00:00 / 00:00")
        layout.addWidget(self.lbl_time)
        
    def setup_connections(self):
        self.btn_play_pause.clicked.connect(self.toggle_playback)
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.playbackStateChanged.connect(self.update_state)
        
        self.slider.sliderMoved.connect(self.set_position)
        
    def toggle_playback(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()
            
    def update_state(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.btn_play_pause.setText("⏸ Pause")
        else:
            self.btn_play_pause.setText("▶ Play")
            
    def update_position(self, position):
        self.slider.blockSignals(True)
        self.slider.setValue(position)
        self.slider.blockSignals(False)
        self.update_time_label()
        
    def update_duration(self, duration):
        self.slider.setRange(0, duration)
        self.update_time_label()
        
    def set_position(self, position):
        self.player.setPosition(position)
        
    def update_time_label(self):
        pos = self.player.position()
        dur = self.player.duration()
        
        def format_time(ms):
            s = int(ms / 1000)
            m = s // 60
            s = s % 60
            return f"{m:02d}:{s:02d}"
            
        self.lbl_time.setText(f"{format_time(pos)} / {format_time(dur)}")
        
    def stop(self):
        self.player.stop()
        
    def hideEvent(self, event):
        # Auto-pause when navigated away
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        super().hideEvent(event)
        
    def stop_and_release(self):
        self.player.stop()
