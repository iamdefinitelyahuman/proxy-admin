import brownie
import pytest
from brownie import ZERO_ADDRESS


def test_initial_getter(proxy):
    assert proxy.get_admin_change_status() == [ZERO_ADDRESS, ZERO_ADDRESS, False]


def test_request_admin(proxy, alice, charlie):
    tx = proxy.request_admin_change(charlie, {"from": alice})

    assert proxy.get_admin_change_status() == [alice, charlie, False]
    assert tx.events["RequestAdminChange"] == [alice, charlie]


def test_request_admin_no_auth(proxy, alice, charlie):
    with brownie.reverts("dev: only admin"):
        proxy.request_admin_change(charlie, {"from": charlie})


@pytest.mark.parametrize("idx", range(2))
def test_request_admin_already_admin(accounts, proxy, alice, idx):
    with brownie.reverts("dev: new admin is already admin"):
        proxy.request_admin_change(accounts[idx], {"from": alice})


def test_request_admin_already_active(proxy, alice, charlie):
    proxy.request_admin_change(charlie, {"from": alice})
    with brownie.reverts("dev: already an active request"):
        proxy.request_admin_change(charlie, {"from": alice})
