import hashlib
import pathlib
import shutil

import pytest

from tests.support.helpers import Webserver
from tests.support.runtests import RUNTIME_VARS


@pytest.fixture(scope="module")
def file(states):
    return states.file


@pytest.fixture
def grail(state_tree):
    src = pathlib.Path(RUNTIME_VARS.BASE_FILES) / "grail"
    dst = state_tree / "grail"
    try:
        shutil.copytree(str(src), str(dst))
        assert dst.exists()
        yield dst
    finally:
        shutil.rmtree(str(dst), ignore_errors=True)


@pytest.fixture
def holy(state_tree_prod):
    src = pathlib.Path(RUNTIME_VARS.PROD_FILES) / "holy"
    dst = state_tree_prod / "holy"
    try:
        shutil.copytree(str(src), str(dst))
        assert dst.exists()
        yield dst
    finally:
        shutil.rmtree(str(dst), ignore_errors=True)


@pytest.fixture
def grail_scene33_file(grail):
    file_obj = grail / "scene33"
    content = file_obj.read_bytes()
    content = content.replace(b"\r\n", b"\n")
    file_obj.write_bytes(content)
    return file_obj


@pytest.fixture
def grail_scene33_clearsign_file(grail_scene33_file):
    file_obj = grail_scene33_file.with_suffix(".clearsign.asc")
    content = file_obj.read_bytes()
    content = content.replace(b"\r\n", b"\n")
    file_obj.write_bytes(content)
    return file_obj


@pytest.fixture
def grail_scene33_file_hash(grail_scene33_file):
    return hashlib.sha256(grail_scene33_file.read_bytes()).hexdigest()


@pytest.fixture
def grail_scene33_clearsign_file_hash(grail_scene33_clearsign_file):
    return hashlib.sha256(grail_scene33_clearsign_file.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def state_file_account():
    with pytest.helpers.create_account(create_group=True) as system_account:
        yield system_account


@pytest.fixture(scope="module")
def webserver(state_tree):
    _webserver = Webserver(root=str(state_tree))
    try:
        _webserver.start()
        yield _webserver
    finally:
        _webserver.stop()
