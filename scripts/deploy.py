from brownie import ProxyAdmin, accounts

DEPLOYER = accounts.at("0x7EeAC6CDdbd1D0B8aF061742D41877D7F707289a", True)
ADMINS = [
    "0x7EeAC6CDdbd1D0B8aF061742D41877D7F707289a",
    "0x7EeAC6CDdbd1D0B8aF061742D41877D7F707289a",
]


def main():
    ProxyAdmin.deploy(ADMINS, {"from": DEPLOYER})
