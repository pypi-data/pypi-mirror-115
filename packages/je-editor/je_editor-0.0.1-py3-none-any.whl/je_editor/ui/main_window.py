import sys
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow

from je_editor.ui.editor import Ui_MainWindow
from je_editor.utils.editor_content.content_save import open_content_and_start
from je_editor.utils.editor_content.content_save import save_content_and_quit
from je_editor.utils.file.open_file import open_file
from je_editor.utils.file.open_file import read_file
from je_editor.utils.file.save_file import SaveThread
from je_editor.utils.file.save_file import save_file
from je_editor.utils.file.save_file import write_file
from je_editor.utils.text_process.exec_text import exec_code
from je_editor.utils.text_process.shell_text import run_on_shell


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        # auto save thread
        self.auto_save_thread = None
        # save file
        self.file = None
        self.ui.setupUi(self)
        # exec code button
        self.ui.code_exec_pushbutton.clicked.connect(self.exec_code_connect)
        # shell button
        self.ui.shell_pushbutton.clicked.connect(self.run_on_shell_connect)
        # menu open file
        self.ui.action_open_file.triggered.connect(self.open_file_connect)
        # menu save file
        self.ui.action_save_file.setShortcut("Ctrl+S")
        self.ui.action_save_file.triggered.connect(self.save_file_connect)
        self.closeEvent = self.close_event
        self.read_editor_setting()

    def read_editor_setting(self):
        temp = open_content_and_start()
        if temp is not None:
            self.file = [temp]
        if self.file is not None:
            read_file(self.file, self.ui.code_edit_plaintext.setPlainText)
            self.start_auto_save()

    def start_auto_save(self):
        if self.auto_save_thread is None and self.file is not None and self.file[0] != "":
            self.auto_save_thread = SaveThread(self.file, self.ui.code_edit_plaintext.toPlainText)
            self.auto_save_thread.start()
        elif self.auto_save_thread is not None:
            self.auto_save_thread.file = self.file

    def exec_code_connect(self):
        exec_code(self.ui.code_edit_plaintext.toPlainText(), self.ui.console_plaintext.setPlainText,
                  self.ui.console_plaintext.setPlainText)

    def run_on_shell_connect(self):
        run_on_shell(self.ui.code_edit_plaintext.toPlainText(), self.ui.console_plaintext.setPlainText,
                     self.ui.console_plaintext.setPlainText)

    def open_file_connect(self):
        self.file = open_file(self.ui.code_edit_plaintext.setPlainText)
        self.start_auto_save()

    def save_file_connect(self):
        self.file = save_file(self.ui.code_edit_plaintext.toPlainText)
        self.start_auto_save()

    def close_event(self, q_close_event):
        if self.file is not None:
            file_path = Path(self.file[0])
            if file_path.exists() and file_path.is_file():
                write_file(self.file, self.ui.code_edit_plaintext.toPlainText)
                save_content_and_quit(self.file)
        sys.exit(0)
