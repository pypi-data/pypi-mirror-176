#!/usr/bin/python

import platform
import requests

from pete_tpl import dll


LIBPETETPL_VERSION = 'v0.5.0'
SUPPORTED_TARGETS = ['x86_64-unknown-linux-gnu', 'x86_64-pc-windows-msvc']
VENDORS = {
    'linux': 'unknown',
    'windows': 'pc',
}
BUILD_SYSTEMS = {
    'linux': 'gnu',  # might be also musl. Probably some additional logic will be needed
    'windows': 'msvc',
}
FILE_EXTENSIONS = {
    'linux': 'so',
    'windows': 'dll',
}
FILE_NAMES = {
    'linux': 'libpetetpl',
    'windows': 'petetpl',
}

OS_ARCHITECTURE = platform.machine().lower()
if OS_ARCHITECTURE == "amd64":
    OS_ARCHITECTURE = "x86_64"

OS_NAME = platform.system().lower()

VENDOR = VENDORS.get(OS_NAME)
if VENDOR is None:
    raise Exception(f"Cannot determine a vendor name for OS: {OS_NAME}")

BUILD_SYSTEM = BUILD_SYSTEMS.get(OS_NAME)
if BUILD_SYSTEM is None:
    raise Exception(f"Cannot determine a build system for OS: {OS_NAME}")

FILE_EXTENSION = FILE_EXTENSIONS.get(OS_NAME)
if FILE_EXTENSION is None:
    raise Exception(f"Cannot determine a library file extension for OS: {OS_NAME}")

FILE_NAME = FILE_NAMES.get(OS_NAME)
if FILE_NAME is None:
    raise Exception(f"Cannot determine a library file name for OS: {OS_NAME}")


def download_shared_lib():
    print("[PETETPL] Downloading the Petetpl shared lib...")
    target = '-'.join([OS_ARCHITECTURE, VENDOR, OS_NAME, BUILD_SYSTEM])
    if target not in SUPPORTED_TARGETS:
        raise Exception(f"Target is '{target}' not supported")

    url = f"https://github.com/pete-tpl/libpetetpl/releases/download/" \
          f"{LIBPETETPL_VERSION}/{FILE_NAME}-{LIBPETETPL_VERSION}-{target}.{FILE_EXTENSION}"
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        raise Exception(f'Failed to download a library: {url}\n'
                        f'HTTP status: {r.status_code}')
    with open(dll.format_shared_lib_path(), 'wb') as f:
        f.write(r.content)
    print("[PETETPL] Downloading complete")


download_shared_lib()
