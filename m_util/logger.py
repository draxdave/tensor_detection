#! /usr/bin/python
import time


class Logger:
    _recorder_file_pointer = ""
    _file_path = 'logs/training_logs.txt'

    def __init__(self, base_path):
        self._file_path = base_path + self._file_path

    def _open_file(self):
        try:
            self._recorder_file_pointer = open(self._file_path, 'a+')

        except FileNotFoundError:
            print("Log File not accessible in : " + self._file_path)
            self._close_file()

    def _close_file(self):
        self._recorder_file_pointer.close()

    def record(self, event):
        self._open_file()
        event = "%s | Logger: Training - %s\n" % (time.asctime(time.localtime(time.time())), event)
        self._recorder_file_pointer.write(event)
        self._close_file()


