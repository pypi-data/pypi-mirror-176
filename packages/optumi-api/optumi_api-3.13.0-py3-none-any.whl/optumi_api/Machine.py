##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

import json, time
from enum import Enum


class Status(Enum):
    ACQUIRING = "Acquiring"
    CONFIGURING = "Configuring"
    BUSY = "Busy"
    IDLE = "Idle"
    RELEASING = "Releasing"


class Machines:
    @classmethod
    def list(cls, status: Status = None):
        machines = []

        response = json.loads(optumi.core.get_machines().text)

        for machine in response["machines"]:
            machine = Machine(*Machine.reconstruct(machine))
            if machine.is_visible():
                machines.append(machine)

        return machines


class Machine:
    def __init__(
        self,
        uuid: str,
        size: str,
        dns_name: str,
        rate: float,
        promo: bool,
        app: str,
        state: str = None,
    ):
        self._uuid = uuid
        self._size = size.replace("Azure:", "AZ:")
        self._dns_name = dns_name
        self._rate = "$" + str(round(rate, 2)) + "/hr"
        self._promo = promo
        self._app = app
        self._state = state
        self._last_refresh = time.time()

    @classmethod
    def reconstruct(cls, machine_map):
        return (
            machine_map["uuid"],
            machine_map["name"],
            machine_map["dnsName"],
            machine_map["rate"],
            machine_map["promo"],
            machine_map["app"],
            machine_map["state"],
        )

    def _refresh(self):
        now = time.time()
        if now - self._last_refresh > 5:
            self._last_refresh = now
            response = json.loads(optumi.core.get_machines().text)
            for machine in response["machines"]:
                if machine["uuid"] == self._uuid:
                    (
                        _,
                        _,
                        self._dns_name,
                        self._rate,
                        self._promo,
                        self._app,
                    ) = Machine.reconstruct(machine)
                    break

    def release(self):
        optumi.core.delete_machine(self._uuid)

    def is_visible(self):
        self._refresh()
        if (
            self._state == "requisition requested"
            or self._state == "requisition in progress"
            or self._state == "requisition completed"
            or self._state == "requisition completed"
            or self._state == "setup completed"
        ):
            return True
        return False

    @property
    def size(self):
        self._refresh()
        return self._size

    @property
    def rate(self):
        self._refresh()
        return self._rate

    @property
    def promo(self):
        self._refresh()
        return self._promo

    @property
    def dns_name(self):
        self._refresh()
        return self._dns_name

    # TODO:JJ Test this
    @property
    def workload(self):
        self._refresh()
        if self._app == None:
            return None
        ws = Workloads.list()
        for w in ws:
            if w.uuid == self._app:
                return w

    @property
    def status(self):
        if self._state in ["requisition requested", "requisition in progress"]:
            return Status.ACQUIRING
        elif self._state in ["requisition completed"]:
            return Status.CONFIGURING
        elif self._state in ["setup completed"]:
            return Status.BUSY if self._app != None else Status.IDLE
        elif self._state in [
            "teardown requested",
            "sequestration requested",
            "sequestration in progress",
            "sequestration completed",
        ]:
            return Status.RELEASING
        else:
            return ""

    def __str__(self):
        return str(self.size) + " " + str(self._rate)
