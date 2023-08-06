# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/20 10:40
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : module.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/20 : create new
# ----------------------------------------------------------------

from .runner import Runner


class Module:

    def __init__(self, runner: Runner):
        self.runner = runner

    def config(self, mid):
        """
        Multi-parameter query, obtaining all the settable parameters for a module.
        :param mid:
        :return:
        """
        cmd = f'{mid} M_CONFIG ?'
        return self.runner.ask(cmd)

    def info(self, mid):
        """
        Multi-parameter query, obtaining all the non-settable parameters for a module.
        :param mid:
        :return:
        """
        cmd = f'{mid} M_INFO ?'
        return self.runner.ask(cmd)

    def reservation(self, mid, whattodo=None):
        """
        You set this parameter to reserve, release, or relinquish a module itself (as opposed to its ports).
        The module must be reserved before its hardware image can be upgraded.
        The owner of the session must already have been specified. Reservation will fail if the chassis or
        any ports are reserved to other users.
        :param whattodo:  coded byte, containing the operation to perform: [RELEASE (0) | RESERVE (1) | RELINQUISH (2)]
        Note: The reservation parameters are slightly asymmetric with respect to set/get.
        When querying for the current reservation state, the chassis will use these
        values: [ RELEASED (0) | RESERVED_BY_YOU (1) | RESERVED_BY_OTHER (2) ]
        :return:
        """
        if whattodo:
            cmd = f'{mid} M_RESERVATION {whattodo}'
            return self.runner.send_expect_ok(cmd)
        else:
            cmd = f'{mid} M_RESERVATION ?'
            return self.runner.ask(cmd)

    def timesync(self, mid, mode):
        """
        Control how the test module time-stamp clock is running, either freely in the chassis or locked to
        an external system time. Running with free chassis time allows nano-second precision
        measurements of latencies, but only when the transmitting and receiving ports are in the same chassis.
        Running with locked external time enables inter-chassis latency measurements, but can introduce small
        time discontinuities as the test module time is adjusted.
        :param mid:
        :param mode:coded byte, selecting the time sync mode: [ CHASSIS | EXTERNAL | MODULE]
        :return:
        """
        cmd = f'{mid} M_TIMESYNC {mode}'
        return self.runner.send_expect_ok(cmd)

    def clockppb(self, mid, ppb):
        """
        Makes small adjustment to the local clock of the test module, which drives the TX rate of the test ports.
        :param mid:
        :param ppb: adjustment from nominal value, in parts-per-billion, positive or negative.
        :return:
        """
        cmd = f'{mid} M_CLOCKPPB {ppb}'
        return self.runner.send_expect_ok(cmd)
