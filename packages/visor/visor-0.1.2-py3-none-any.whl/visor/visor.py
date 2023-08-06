from pathlib import Path
import datetime as dt
import uuid
from dataclasses import dataclass, field
from typing import *
import subprocess
import io
import os
import shlex
import signal
import time


__all__ = ['Visor']

ROOT_LOG_DIR = Path(".visor-logs").absolute()

def _current_log_dir():
    _uid = uuid.uuid4()
    log_id = _uid.hex[:7]
    dir_name = f"{log_id}-{dt.datetime.now().strftime('%Y.%m.%d-%H.%M.%S')}"
    log_dir = ROOT_LOG_DIR/dir_name
    log_dir.mkdir(exist_ok=True, parents=True)
    return log_dir


@dataclass
class Visor:
    active: List[subprocess.Popen] = field(default_factory=list)
    log_dir: Path = field(default_factory=_current_log_dir)
    _log_fds: List[Tuple[io.BufferedWriter, io.BufferedWriter]] = field(default_factory=list)

    def get_log_files(self, process: subprocess.Popen) -> Tuple[Path, Path]:
        id = None
        for i, p in enumerate(self.active):
            if p.pid == process.pid:
                id = i
                break
        assert id != None
        return self._get_log_files(id)


    def add(self, command: 'str') -> subprocess.Popen:
        """Runs command through shell"""
        # setsid: https://stackoverflow.com/a/4791612/10120928
        outf, errf = self._get_log_fds(len(self.active))
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid, stdout=outf, stderr=errf)
        self._log_fds.append((outf, errf))

        self.active.append(process)
        return process

    def add_raw(self, command: 'str | List[str]') -> subprocess.Popen:
        """Directly passes command to Popen"""
        command = self._split_command(command)

        outf, errf = self._get_log_fds(len(self.active))
        process = subprocess.Popen(command, preexec_fn=os.setsid, stdout=outf, stderr=errf)
        self._log_fds.append((outf, errf))

        self.active.append(process)
        return process
    
    def _communicate(self, process: subprocess.Popen):
        try:
            process.communicate(timeout=0)
        except subprocess.TimeoutExpired:
            return

    def show(self):
        for process in self.active:
            self._communicate(process)
            print(self._repr_process(process))
    
    def kill_all(self, signal: int = signal.SIGKILL):
        for process in self.active:
            if not isinstance(process.returncode, int):
                self._kill(process, signal)

    def terminate_all(self):
        for process in self.active:
            if not isinstance(process.returncode, int):
                self._kill(process, signal.SIGTERM)
    
    def wait(self, timeout: 'float| None' = None):
        start_time = time.time()
        for process in self.active:
            if not isinstance(process.returncode, int):
                if timeout != None:
                    child_timeout =  max(0, (start_time + timeout) - time.time())
                else:
                    child_timeout = None
                process.wait(timeout = child_timeout)

    def _get_log_fds(self, id: int) -> Tuple[io.BufferedWriter, io.BufferedWriter]:
        outl, errl = self._get_log_files(id)
        return open(outl, 'ab'), open(errl, 'ab')

    def _get_log_files(self, id: int) -> Tuple[Path, Path]:
        return (self.log_dir/f'{id}.log', self.log_dir/f'{id}.err.log')

    @staticmethod
    def _repr_process(process: subprocess.Popen) -> str:
        return f"{process.pid}: {process.returncode} ({process.args})"

    @staticmethod
    def _kill(process: subprocess.Popen, signal: int = signal.SIGTERM):
        """
            Kills the process group. NOTE: only to be used if process has
            been started with a seperate sid, otherwise it'll kill current python process
            also
        """
        gid = os.getpgid(process.pid)
        os.killpg(gid, signal)

    @staticmethod
    def _split_command(command: 'str | List[str]') -> List[str]:
        if isinstance(command, str):
            return shlex.split(command)
        return command

