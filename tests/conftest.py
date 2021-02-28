import pytest


@pytest.fixture(autouse=True)
def setup_isolation(fn_isolation):
    pass


@pytest.fixture(scope="session")
def alice(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def bob(accounts):
    yield accounts[1]


@pytest.fixture(scope="session")
def charlie(accounts):
    yield accounts[2]


@pytest.fixture(scope="session")
def dave(accounts):
    yield accounts[4]


@pytest.fixture(scope="module")
def proxy(ProxyAdmin, alice, bob):
    yield ProxyAdmin.deploy([alice, bob], {"from": alice})
