import brownie
import pytest
from brownie import compile_source, history
from brownie.test import given, strategy


@pytest.fixture(scope="module")
def target(alice):
    source = """

pragma solidity 0.8.0;

contract Tester {

    event Data (
        bytes data,
        uint256 value
    );

    fallback() external payable {
        emit Data(msg.data, msg.value);
    }

    function doNotPass() external {
        revert();
    }

    function hasReturnData() external returns (uint256) {
        return 42;
    }
}
    """
    Tester = compile_source(source).Tester
    yield Tester.deploy({"from": alice})


@given(
    st_calldata=strategy("bytes", min_size=8, max_size=10000),
    st_value=strategy("uint256", max_value=10 ** 18),
)
def test_execute(proxy, alice, target, st_calldata, st_value):
    tx = proxy.execute(target, st_calldata, {"from": alice, "value": st_value})

    assert tx.events["Data"] == [f"0x{st_calldata.hex()}", st_value]
    assert tx.events["TransactionExecuted"] == [alice, target, f"0x{st_calldata.hex()}", st_value]


def test_return_data(proxy, bob, target):
    tx = proxy.execute(target, target.hasReturnData.signature, {"from": bob})
    assert tx.subcalls[0]["function"] == "hasReturnData()"


def test_execute_reverts(proxy, alice, target):
    with brownie.reverts():
        proxy.execute(target, target.doNotPass.signature, {"from": alice})
    assert history[-1].subcalls[0]["function"] == "doNotPass()"


def test_only_admin(proxy, charlie, target):
    with brownie.reverts("dev: only admin"):
        proxy.execute(target, "", {"from": charlie})
