import io
import re
import os
import sys
import time
import zlib
import base64
import marshal
from pkgutil import read_code

from uncompyle6 import PYTHON_VERSION
from uncompyle6.main import decompile

ENCODEING = "utf-8"
ALGORITHOMS = (
    "zlib",
    "marshal",
    "base16",
    "base32",
    "base64",
    "base85",
    "machine_code"
)


class CodeSearchAlgorithms:
    @staticmethod
    def bytecode(string: str) -> bytes:
        pattern: str = r"""(((b|bytes\()["'])(.+)(["']))"""
        string_data = re.findall(pattern, string)[0][3]
        return eval(f"b'{string_data}'")

    @staticmethod
    def base64_hash(string: str) -> str:
        pattern: str = r"""((?:(?:b|bytes\()?["'])([a-zA-Z0-9\=\+\/]+)(?:["']))"""
        string_data = re.findall(pattern, string)[0][1]
        return string_data


class DecodingAlgorithms:
    def __init__(self, file_data, save_file):
        self.file_data = file_data
        print("Finding the best algorithm:")
        for algogithom in ALGORITHOMS:
            try:
                self.file_data = self.__getattribute__(algogithom)()
                print(f"# \033[1;32m{algogithom} ✓\033[0m", end="\r")
            except Exception:
                print(f"# \033[1;31m{algogithom}\033[0m")
                continue

            layers: int = 0
            while True:
                try:
                    self.file_data = self.__getattribute__(algogithom)()
                    layers += 1
                    print(f"# \033[1;32m{algogithom} layers {layers} ✓\033[0m", end="\r")
                    time.sleep(.02)
                except Exception:
                    print(f"\n# \033[1;32mDONE ✓\033[0m")
                    break
            break
        try:
            with open(save_file, "w") as file:
                file.write(self.file_data)
        except Exception:
            print("# \033[1;31mFailed to decode the file!\033[0m")

    def marshal(self) -> str:
        bytecode = marshal.loads(CodeSearchAlgorithms.bytecode(self.file_data))
        out = io.StringIO()
        version = PYTHON_VERSION if PYTHON_VERSION < 3.9 else 3.8
        decompile(version, bytecode, out, showast=False)
        return out.getvalue() + '\n'

    def zlib(self) -> str:
        return zlib.decompress(
            CodeSearchAlgorithms.bytecode(self.file_data)
        ).decode(ENCODEING)

    def base16(self) -> str:
        return base64.b16decode(
            CodeSearchAlgorithms.base64_hash(self.file_data)
        ).decode(ENCODEING)

    def base32(self) -> str:
        return base64.b32decode(
            CodeSearchAlgorithms.base64_hash(self.file_data)
        ).decode(ENCODEING)

    def base64(self) -> str:
        return base64.b64decode(
            CodeSearchAlgorithms.base64_hash(self.file_data)
        ).decode(ENCODEING)

    def base85(self) -> str:
        return base64.b85decode(
            CodeSearchAlgorithms.base64_hash(self.file_data)
        ).decode(ENCODEING)

    def machine_code(self) -> str:
        out = io.StringIO()
        version = PYTHON_VERSION if PYTHON_VERSION < 3.9 else 3.8
        decompile(version, self.file_data, out, showast=False)
        data = out.getvalue() + '\n'
        if self.file_data == data:
            raise Exception()
        return data


if __name__ == '__main__':
    # sys.argv.append("/home/psh-team/Downloads/Telegram Desktop/converM.py")
    # sys.argv.append("/home/psh-team/Downloads/Telegram Desktop/newfile(1)-marshal.py")
    # sys.argv.append("/home/psh-team/Downloads/Telegram Desktop/Kai-Hash.py")
    # sys.argv.append("/home/psh-team/Downloads/Telegram Desktop/__pycache__/converM.cpython-38.pyc")
    # sys.argv.append("/home/psh-team/Documents/GitHub/HackerMode/venv/lib/python3.8/site-packages/bidi/__pycache__/__init__.cpython-38.pyc")
    # sys.argv.append("/home/psh-team/Downloads/Telegram Desktop/lambdaa.pyc")
    # sys.argv.append("/home/psh-team/Downloads/Telegram Desktop/output.py")
    if len(sys.argv) > 2:
        if not os.path.isfile(sys.argv[1]):
            exit(f"# file not found!: {sys.argv[1]}")
        try:
            with open(sys.argv[1], "r") as file:
                data = file.read()
        except UnicodeDecodeError:
            with io.open_code(sys.argv[1]) as f:
                data = read_code(f)
        DecodingAlgorithms(data, sys.argv[2])
    else:
        print("USAGE:\n decode file.py output.py")
