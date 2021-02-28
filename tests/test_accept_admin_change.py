import brownie
import pytest
from brownie import ZERO_ADDRESS


@pytest.mark.parametrize("request_idx,approve_idx", [(0, 1), (1, 0)])
def test_approve_admin_change(accounts, proxy, charlie, request_idx, approve_idx):
    proxy.request_admin_change(charlie, {"from": accounts[request_idx]})
    proxy.approve_admin_change({"from": accounts[approve_idx]})

    tx = proxy.accept_admin_change({"from": charlie})

    assert proxy.admins(request_idx) == charlie
    assert proxy.admins(approve_idx) == accounts[approve_idx]

    assert proxy.get_admin_change_status() == [ZERO_ADDRESS, ZERO_ADDRESS, False]
    assert tx.events["AcceptAdminChange"] == [accounts[request_idx], charlie]


def test_no_approval(accounts, proxy, alice, charlie):
    proxy.request_admin_change(charlie, {"from": alice})

    with brownie.reverts("dev: change not approved"):
        proxy.accept_admin_change({"from": charlie})


def test_approval_was_revoked(accounts, proxy, alice, bob, charlie):
    proxy.request_admin_change(charlie, {"from": alice})
    proxy.approve_admin_change({"from": bob})
    proxy.revoke_admin_change({"from": alice})

    with brownie.reverts("dev: change not approved"):
        proxy.accept_admin_change({"from": charlie})


@pytest.mark.parametrize("idx", range(5))
def test_only_new_admin(accounts, proxy, alice, bob, charlie, idx):
    proxy.request_admin_change(charlie, {"from": alice})
    proxy.approve_admin_change({"from": bob})
    if accounts[idx] == charlie:
        proxy.accept_admin_change({"from": accounts[idx]})
    else:
        with brownie.reverts("dev: only new admin"):
            proxy.accept_admin_change({"from": accounts[idx]})
