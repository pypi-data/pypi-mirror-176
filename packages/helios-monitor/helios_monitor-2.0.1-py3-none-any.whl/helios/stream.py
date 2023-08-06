from threading import Thread
from subprocess import Popen, PIPE
from shlex import quote
from datetime import datetime, timedelta

from .utils import process_line


class Stream(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, *, daemon=None):
        super().__init__(group=group, target=target,
                         name=name, daemon=daemon)
        self.stream = args[0]
        self.logger = kwargs["logger"]
        self.is_running = True
        self.current_line = None
        self.max_silence_duration = timedelta(seconds=10)
        self.current_silence = timedelta()

    def run(self):
        self.logger.info("Monitoring stream")
        self.process = self.ffmpeg_process()
        last_update = datetime.now()
        while self.is_running:
            if self.process.poll():
                self.logger.warning("Stream failed, restarting...")
                self.process = self.ffmpeg_process()
            # TODO: readline blocks, which can be problematic if the output is
            # blocked. It should implement a timeout waiting for lines.
            # Or move time monitoring to outside of the Thread and re-create it
            self.current_line = process_line(self.process.stderr.readline())
            if self.current_line == None:
                self.current_silence += datetime.now() - last_update
                print(self.current_silence)
                if self.current_silence > self.max_silence_duration:
                    # Stream has stuck
                    self.logger.warning(f"Stream not generating loudness levels for {self.max_silence_duration.seconds} seconds. Restarting...")
                    self.process.kill()
                    self.process = self.ffmpeg_process()
            else:
                self.current_silence = timedelta()
            last_update = datetime.now()


    def ffmpeg_process(self):
        command = ['ffmpeg',
                   '-nostats',
                   '-hide_banner',
                   '-i', quote(self.stream),
                   '-filter_complex',
                   'ebur128=peak=true',
                   '-f', 'null', '-']
        self.logger.debug(f"ffmpeg command: {command}")
        self.current_silence = timedelta()
        return Popen(command,
                     stdout=PIPE,
                     stderr=PIPE,
                     universal_newlines=True)
