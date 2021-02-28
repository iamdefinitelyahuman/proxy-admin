# @version 0.2.11

admins: public(address[2])

pending_current_admin: uint256
pending_new_admin: address
change_approved: bool


@external
def __init__(_authorized: address[2]):
    self.admins = _authorized


@payable
@external
def execute(_target: address, _calldata: Bytes[100000]):
    assert msg.sender in self.admins  # dev: only admin
    raw_call(_target, _calldata, value=msg.value)


@view
@external
def get_admin_change_status() -> (address, address, bool):
    idx: uint256 = self.pending_current_admin
    if idx == 0:
        return ZERO_ADDRESS, ZERO_ADDRESS, False
    else:
        return self.admins[idx - 1], self.pending_new_admin, self.change_approved


@external
def request_admin_change(_new_admin: address):
    assert self.pending_current_admin == 0  # dev: already an active request

    admin_list: address[2] = self.admins
    assert _new_admin not in admin_list  # dev: new admin is already admin
    for i in range(2):
        if admin_list[i] == msg.sender:
            self.pending_current_admin = i + 1
            self.pending_new_admin = _new_admin
            return
    raise  # dev: only admin


@external
def approve_admin_change():
    idx: uint256 = self.pending_current_admin
    assert idx > 0  # dev: no active request
    assert msg.sender == self.admins[idx % 2]  # dev: caller is not 2nd admin
    self.change_approved = True


@external
def revoke_admin_change():
    assert msg.sender in self.admins  # dev: only admin
    self.pending_current_admin = 0
    self.pending_new_admin = ZERO_ADDRESS
    self.change_approved = False


@external
def accept_admin_change():
    assert self.change_approved == True  # dev: change not approved
    assert msg.sender == self.pending_new_admin  # dev: only new admin
    self.admins[self.pending_current_admin - 1] = msg.sender

    self.pending_current_admin = 0
    self.pending_new_admin = ZERO_ADDRESS
    self.change_approved = False
