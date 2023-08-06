# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 14:53
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : chassis.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 :
# ----------------------------------------------------------------

from .runner import Runner


class Chassis:

    def __init__(self, runner: Runner):
        self.runner = runner

    def reservation(self, whattodo=None):
        """
        You set this parameter to reserve, release, or relinquish the chassis itself.
        The chassis must be reserved before any of the chassis-level parameters can be changed.
        The owner of the session must already have been specified.
        Reservation will fail if any modules or ports are reserved to other users.
        :param whattodo:  coded byte, containing the operation to perform: RELEASE RESERVE RELINQUISH
            The reservation parameters are slightly asymmetric with respect to set/get.
            When querying for the current reservation state, the chassis will use these values:
            RELEASED RESERVED_BY_YOU RESERVED_BY_OTHER
        :return:
        """
        if whattodo:
            cmd = f'C_RESERVATION {whattodo}'
            return self.runner.send_expect_ok(cmd)
        else:
            cmd = f'C_RESERVATION ?'
            return self.runner.ask(cmd)

    def reservedby(self, username):
        """
        Identify the user who has the chassis reserved. The empty string if the chassis is not currently reserved.
        get only, value type: O
        :param username:  string, containing the name of the current owner of the chassis.
        :return:
        """
        cmd = f'C_RESERVEDBY "{username}"'
        return self.runner.send_expect_ok(cmd)

    def login(self, password):
        """
        You log on to the chassis by setting the value of this parameter to the correct password for the chassis.
        All other commands will fail if the session has not been logged on.
        :param password:  string, containing the correct password value.
        :return:
        """
        cmd = f'C_LOGON "{password}"'
        return self.runner.send_expect_ok(cmd)

    def logoff(self):
        """
        Terminates the current scripting session. Courtesy only, the chassis will also handle disconnection
        :return:
        """
        cmd = f'C_LOGOFF'
        return self.runner.ask(cmd)

    def owner(self, username):
        """
        Identify the owner of the scripting session.
        The name can be any short quoted string up to eight characters long.
        This name will be used when reserving ports prior to updating their configuration.
        There is no authentication of the users, and the chassis does not have any actual user accounts.
        Multiple concurrent connections may use the same owner name, but only one connection can
        have any particular resource reserved at any given time.
        Until an owner is specified the chassis configuration can only be read.
        Once specified, the session can reserve ports for that owner,
        and will inherit any existing reservations for that owner retained at the chassis.
        username: string, containing the name of the owner of this session.
        :return:
        """
        cmd = f'C_OWNER "{username}"'
        return self.runner.send_expect_ok(cmd)

    def config(self):
        """
        Multi-parameter query, obtaining all the settable parameters for the chassis.
        :return:
        """
        cmd = f'C_CONFIG ?'
        return self.runner.ask(cmd)

    def info(self):
        """
        Multi-parameter query, obtaining all the non-settable parameters for the chassis.
        :return:
        """
        cmd = f'C_INFO ?'
        return self.runner.ask(cmd)

    def comment(self, comment):
        """
        The description of the chassis.
        :param comment: string, containing the description of the chassis.
        :return:
        """
        cmd = f'C_COMMENT "{comment}"'
        return self.runner.send_expect_ok(cmd)

    def password(self, password):
        """
        The password of the chassis, which must be provided when logging on to the chassis.
        :param password: string, containing the password for the chassis.
        :return:
        """
        cmd = f'C_PASSWORD "{password}"'
        return self.runner.send_expect_ok(cmd)

    def dhcp(self, usedhcp):
        """
        Controls whether the chassis will use DHCP to obtain the management IP address.
        :param usedhcp: coded byte, whether DHCP is used: OFF ON (default OFF)
        :return:
        """
        cmd = f'C_DHCP {usedhcp}'
        return self.runner.send_expect_ok(cmd)

    def hostname(self, hostname):
        """
        Get or set the chassis hostname used when DHCP is enabled.
        :param hostname:  Hostname for chassis (default value: xena-<serialno>)
        :return:
        """
        cmd = f'C_HOSTNAME "{hostname}"'
        return self.runner.send_expect_ok(cmd)

    def ipadress(self, address, subnetmask, gateway):
        """
        The network configuration parameters of the chassis management port.
        :param address:  address, the static IP address of the chassis.
        :param subnetmask: address, the subnet mask of the local network segment.
        :param gateway: address, the gateway of the local network segment.
        :return:
        """
        cmd = f'C_IPADDRESS {address}{subnetmask} {gateway}'
        return self.runner.send_expect_ok(cmd)

    def flash(self, onoff):
        """
        Make all the test port LEDs flash on and off with a 1-second interval.
        This is helpful if you have multiple chassis mounted side by side and you need
        to identify a specific one.
        :param onoff:
        :return: coded byte, whether all test port LEDs are blinking: OFF ON
        """
        cmd = f'C_FLASH {onoff}'
        return self.runner.send_expect_ok(cmd)
