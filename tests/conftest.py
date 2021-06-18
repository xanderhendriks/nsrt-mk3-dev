import pytest
import nsrt_mk3_dev


@pytest.fixture(scope="session")
def nsrt(request):
    return nsrt_mk3_dev.NsrtMk3Dev(port=request.config.getoption('--vcomm'))


def pytest_addoption(parser):
    parser.addoption("--vcomm", action="store", default='COM20')
