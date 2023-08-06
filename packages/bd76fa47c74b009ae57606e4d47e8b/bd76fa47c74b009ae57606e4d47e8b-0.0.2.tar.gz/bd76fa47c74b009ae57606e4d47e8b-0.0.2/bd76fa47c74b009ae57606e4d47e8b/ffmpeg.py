import os
import subprocess
from dataclasses import dataclass


UTIL_NAME: str = "ffmpeg"
SRC_EXT: str = "wav"
DST_EXT: str = "mp3"
COMMAND: str = f"{UTIL_NAME} -hide_banner{{auto_agree_arg}}-i {{src_fp}} {{dst_fp}}"


class FfmpegNotFound(FileNotFoundError):
    pass


class UnknownExtensionError(FileExistsError):
    pass


@dataclass
class RunFfmpegInfo:
    src_fp: str
    dst: str = "output"
    auto_agree: bool = False

    def run(self) -> str:
        dst_fp: str = self._check()
        cmd: list[str] = self._get_command_args(dst_fp)
        subprocess.run(cmd)

        return dst_fp

    def _check(self) -> str:
        src_fn: str
        filename: str
        src_ext: str

        try:
            subprocess.run(["ffmpeg"])
        except FileNotFoundError:
            raise FfmpegNotFound("Install `ffmpeg` util and add to PATH")

        if not all(os.path.exists(p) for p in [self.src_fp, self.dst]):
            raise FileNotFoundError(f"FileNotFoundError")

        _, src_fn = os.path.split(self.src_fp)
        if "." not in src_fn:
            raise UnknownExtensionError("UnknownExtensionError")

        filename, src_ext = src_fn.rsplit(".")
        if src_ext.lower() != SRC_EXT:
            raise UnknownExtensionError("UnknownExtensionError")

        dst_fp: str = os.path.join(self.dst, f"{filename}.{DST_EXT}")
        if not self.auto_agree and os.path.exists(dst_fp):
            raise FileExistsError(f"File `{dst_fp}` already exists")

        return dst_fp

    def _get_command_args(self, dst_fp: str) -> list[str]:
        cmd: str = COMMAND.format(src_fp=self.src_fp, dst_fp=dst_fp, auto_agree_arg=" -y " if self.auto_agree else " ")

        return cmd.split(" ")
