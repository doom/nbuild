#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import core
import ntpath
import shutil
import hashlib
import requests
import ftplib
import stdlib
from urllib.parse import urlparse
from core.log import wlog, ilog, clog, flog


def fetch_data():
    build = stdlib.current_build()

    datas = build.version_data.get('fetch_urls', None)
    if datas is not None:
        urls(datas)

    data = build.version_data.get('fetch_url', None)
    if data is not None:
        url(**data)


def urls(
    downloads,
):
    for download in downloads:
        url(**download)


def url(
    url: str,
    md5=None,
    sha1=None,
    sha256=None,
):
    build = stdlib.current_build()

    url_object = urlparse(url)
    path = os.path.join(
        build.download_cache,
        os.path.basename(url_object.path)
    )

    if not sha256:
        wlog(f"No sha256 to ensure the integrity of {url}")

    if not _check_file(path, md5, sha1, sha256):
        ilog(f"Fetching {url}")
        if url_object.scheme == 'http' or url_object.scheme == 'https':
            _download_http(url, path)
        elif url_object.scheme == ('ftp'):
            _download_ftp(url_object, path)
        else:
            flog(f"Unknown protocol to download file from url {url}")
            exit(1)
        clog(f"Fetch done. Stored at {path}")
        if not _check_file(path, md5, sha1, sha256):
            flog(
                "Downloaded file's signature is invalid. "
                "Please verify the signature(s) in the build manifest "
                "and the authenticity of the given link."
            )
            exit(1)
    else:
        clog(f"Using cache at {path}")


def _download_http(url, path):
        req = requests.get(url, stream=True)
        with open(path, 'wb') as file:
            for chunk in req.iter_content(chunk_size=4096):
                file.write(chunk)


def _download_ftp(url_object, path):
    ftp = ftplib.FTP(url_object.netloc)
    ftp.login()
    with open(path, 'wb') as out_file:
        ftp.retrbinary(
                f'RETR {url_object.path}',
                lambda data: out_file.write(data),
                blocksize=4096,
        )


def _check_file(path, md5, sha1, sha256):
    if os.path.exists(path):
        out = True
        if md5 is not None:
            out &= _check_md5(path, md5)
        if sha1 is not None:
            out &= _check_sha1(path, sha1)
        if sha256 is not None:
            out &= _check_sha256(path, sha256)
        return out
    else:
        return False


def _check_md5(path, md5):
    hash_md5 = hashlib.md5()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest() == md5


def _check_sha1(path, sha1):
    hash_sha1 = hashlib.sha1()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest() == sha1


def _check_sha256(path, sha256):
    hash_sha256 = hashlib.sha256()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest() == sha256


def add_file(*paths):
    build = stdlib.current_build()

    for path in paths:
        if os.path.isabs(path):
            raise RuntimeError("add_file() received an absolute path as parameter, while it expects a relative one")
        filename = ntpath.basename(path)
        dirname = ntpath.dirname(path)
        dstdir = os.path.join(
            build.build_cache,
            dirname,
        )
        dstpath = os.path.join(
            dstdir,
            filename,
        )
        srcpath = os.path.join(
            os.path.dirname(build.manifest.path),
            path,
        )
        os.makedirs(dstdir, exist_ok=True)
        shutil.copyfile(srcpath, dstpath)
