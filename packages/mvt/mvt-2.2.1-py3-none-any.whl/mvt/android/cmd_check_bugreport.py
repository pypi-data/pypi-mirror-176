# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2022 Claudio Guarnieri.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging
import os
from pathlib import Path
from typing import Callable, Optional
from zipfile import ZipFile

from mvt.common.command import Command

from .modules.bugreport import BUGREPORT_MODULES

log = logging.getLogger(__name__)


class CmdAndroidCheckBugreport(Command):

    def __init__(
        self,
        target_path: Optional[str] = None,
        results_path: Optional[str] = None,
        ioc_files: Optional[list] = None,
        module_name: Optional[str] = None,
        serial: Optional[str] = None,
        fast_mode: Optional[bool] = False,
    ) -> None:
        super().__init__(target_path=target_path, results_path=results_path,
                         ioc_files=ioc_files, module_name=module_name,
                         serial=serial, fast_mode=fast_mode, log=log)

        self.name = "check-bugreport"
        self.modules = BUGREPORT_MODULES

        self.bugreport_format = None
        self.bugreport_archive = None
        self.bugreport_files = []

    def init(self) -> None:
        if os.path.isfile(self.target_path):
            self.bugreport_format = "zip"
            self.bugreport_archive = ZipFile(self.target_path)
            for file_name in self.bugreport_archive.namelist():
                self.bugreport_files.append(file_name)
        elif os.path.isdir(self.target_path):
            self.bugreport_format = "dir"
            parent_path = Path(self.target_path).absolute().as_posix()
            for root, _, subfiles in os.walk(os.path.abspath(self.target_path)):
                for file_name in subfiles:
                    file_path = os.path.relpath(os.path.join(root, file_name),
                                                parent_path)
                    self.bugreport_files.append(file_path)

    def module_init(self, module: Callable) -> None:
        if self.bugreport_format == "zip":
            module.from_zip(self.bugreport_archive, self.bugreport_files)
        else:
            module.from_folder(self.target_path, self.bugreport_files)

    def finish(self) -> None:
        if self.bugreport_archive:
            self.bugreport_archive.close()
