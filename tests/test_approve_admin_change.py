import brownie
import pytest


@pytest.mark.parametrize("request_idx,approve_idx", [(0, 1), (1, 0)])
def test_approve_admin_change(accounts, proxy, charlie, request_idx, approve_idx):
    proxy.request_admin_change(charlie, {"from": accounts[request_idx]})
    tx = proxy.approve_admin_change({"from": accounts[approve_idx]})

    assert proxy.get_admin_change_status() == [accounts[request_idx], charlie, True]
    assert tx.events["ApproveAdminChange"] == [
        accounts[request_idx],
        charlie,
        accounts[approve_idx],
    ]


def test_no_active_request(proxy, alice, charlie):
    with brownie.reverts("dev: no active request"):
        proxy.approve_admin_change({"from": alice})


@pytest.mark.parametrize("idx", range(2))
def test_wrong_admin(accounts, proxy, charlie, idx):
    proxy.request_admin_change(charlie, {"from": accounts[idx]})
    with brownie.reverts("dev: caller is not 2nd admin"):
        proxy.approve_admin_change({"from": accounts[idx]})


@pytest.mark.parametrize("idx", range(2, 5))
def test_not_an_admin(accounts, proxy, alice, charlie, idx):
    proxy.request_admin_change(charlie, {"from": alice})
    with brownie.reverts("dev: caller is not 2nd admin"):
        proxy.approve_admin_change({"from": accounts[idx]})
