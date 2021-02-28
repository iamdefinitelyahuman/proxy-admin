import brownie
import pytest
from brownie import ZERO_ADDRESS


@pytest.mark.parametrize("request_idx,approve_idx", [(0, 1), (1, 0)])
@pytest.mark.parametrize("revoke_idx", range(2))
def test_revoke_after_approve(accounts, proxy, charlie, request_idx, approve_idx, revoke_idx):
    proxy.request_admin_change(charlie, {"from": accounts[request_idx]})
    proxy.approve_admin_change({"from": accounts[approve_idx]})
    proxy.revoke_admin_change({"from": accounts[revoke_idx]})

    assert proxy.get_admin_change_status() == [ZERO_ADDRESS, ZERO_ADDRESS, False]


def test_revoke_without_request(proxy, alice):
    proxy.revoke_admin_change({"from": alice})

    assert proxy.get_admin_change_status() == [ZERO_ADDRESS, ZERO_ADDRESS, False]


@pytest.mark.parametrize("request_idx", range(2))
@pytest.mark.parametrize("revoke_idx", range(2))
def test_revoke_after_request(accounts, proxy, charlie, request_idx, revoke_idx):
    proxy.request_admin_change(charlie, {"from": accounts[request_idx]})
    proxy.revoke_admin_change({"from": accounts[revoke_idx]})

    assert proxy.get_admin_change_status() == [ZERO_ADDRESS, ZERO_ADDRESS, False]


def test_not_an_admin(proxy, charlie):
    with brownie.reverts("dev: only admin"):
        proxy.revoke_admin_change({"from": charlie})
