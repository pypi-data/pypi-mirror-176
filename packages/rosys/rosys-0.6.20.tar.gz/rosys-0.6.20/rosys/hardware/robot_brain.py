import logging
import os
import sys
from typing import Optional

from nicegui import ui

import rosys

from ..event import Event
from .communication import Communication
from .lizard_firmware import LizardFirmware


class RobotBrain:
    '''This module manages the communication with a [Zauberzeug Robot Brain](https://zauberzeug.com/robot-brain.html).

    It expects a communication object, which is used for the actual read and write operations.
    Besides providing some basic methods like configuring or restarting the microcontroller, it augments and verifies checksums for each message.
    '''

    def __init__(self, communication: Communication, lizard_startup: str = 'lizard.txt') -> None:
        self.LINE_RECEIVED = Event()
        '''a line has been received from the microcontroller (argument: line as string)'''

        self.communication = communication
        self.lizard_startup = lizard_startup
        self.waiting_list: dict[str, Optional[str]] = {}
        self.clock_offset: Optional[float] = None
        self.hardware_time: Optional[float] = None
        self.log = logging.getLogger('rosys.robot_rain')
        self.lizard_firmware = LizardFirmware(self)

    def developer_ui(self) -> None:
        ui.label('Lizard') \
            .bind_text_from(self.lizard_firmware, 'lizard_version', backward=lambda x: f'Lizard ({x or "?"})')
        ui.button('Configure', on_click=self.configure).props('outline')
        ui.button('Restart', on_click=self.restart).props('outline')
        ui.button(f'Update Local ({self.lizard_firmware.available_lizard_version})',
                  on_click=self.lizard_firmware.flash).props('outline')
        ui.button('Update from GitHub', on_click=self.lizard_firmware.update_lizard).props('outline').bind_text_from(
            self.lizard_firmware, 'latest_lizard_release', backward=lambda x: f'Update from GitHub ({x or "?"})')
        ui.button('Enable', on_click=self.enable_esp).props('outline')
        ui.label().bind_text_from(self, 'clock_offset', lambda offset: f'Clock offset: {offset or 0:.3f} s')

    async def configure(self) -> None:
        self.log.info('Configuring...')
        await self.send(f'!-')
        with open(self.lizard_startup) as f:
            for line in f.read().splitlines():
                await self.send(f'!+{line}')
        await self.send(f'!.')
        await self.restart()

    async def restart(self) -> None:
        await self.send(f'core.restart()')

    async def read_lines(self) -> list[tuple[float, str]]:
        lines: list[tuple[float, str]] = []
        millis = None
        while True:
            unchecked = await self.communication.read()
            line = check(unchecked)
            if not line:
                break
            words = line.split()
            if not words:
                continue
            first = words.pop(0)
            if first in self.waiting_list:
                self.waiting_list[first] = line
            if first == 'core':
                millis = float(words.pop(0))
                if self.clock_offset is None:
                    continue
                self.hardware_time = millis / 1000 + self.clock_offset
            self.LINE_RECEIVED.emit(line)
            lines.append((self.hardware_time, line))
        if millis is not None:
            self.clock_offset = rosys.time() - millis / 1000
        return lines

    async def send(self, msg: str) -> None:
        await self.communication.send(augment(msg))

    async def send_and_await(self, msg: str, ack: str, *, timeout: float = float('inf')) -> Optional[str]:
        self.waiting_list[ack] = None
        await self.send(msg)
        t0 = rosys.time()
        while self.waiting_list.get(ack) is None and rosys.time() < t0 + timeout:
            await rosys.sleep(0.1)
        return self.waiting_list.pop(ack) if ack in self.waiting_list else None

    def enable_esp(self) -> None:
        try:
            sys.path.insert(1, os.path.expanduser('~/.lizard'))
            from esp import Esp
            esp = Esp()
            with esp.pin_config():
                esp.activate()
        except:
            self.log.exception('Could not enable ESP')

    def __del__(self) -> None:
        self.communication.disconnect()

    def __repr__(self) -> str:
        return f'<RobotBrain {self.communication}>'


def augment(line: str) -> str:
    checksum = 0
    for c in line:
        checksum ^= ord(c)
    return f'{line}@{checksum:02x}'


def check(line: Optional[str]) -> str:
    if line is None:
        return ""
    if line[-3:-2] == '@':
        check = int(line[-2:], 16)
        line = line[:-3]
        checksum = 0
        for c in line:
            checksum ^= ord(c)
        if checksum != check:
            return None
    return line
