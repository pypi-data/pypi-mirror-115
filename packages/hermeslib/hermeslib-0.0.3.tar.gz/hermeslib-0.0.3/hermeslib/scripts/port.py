# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 14:50
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : port.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 :
# ----------------------------------------------------------------

from .runner import Runner


class Port:

    def __init__(self, runner: Runner):
        self.runner = runner

    def reservation(self, port, whattodo=None):
        """
        You set this parameter to reserve, release, or relinquish a port. The port must be reserved before any of its
        configuration can be changed, including streams, filters, capture, and datasets. The owner of the session must
        already have been specified. Reservation will fail if the chassis or module is reserved to other users.
        :param port:
        :param whattodo: value: coded byte, containing the operation to perform: RELEASE RESERVE RELINQUISH The
                    reservation parameters are slightly asymmetric with respect to set/get. When querying for
                    the current reservation state, the chassis will use these values: RELEASED RESERVED_BY_YOU RESERVED_BY_OTHER
        :return:
        """
        if whattodo:
            cmd = f'{port} P_RESERVATION {whattodo}'
            return self.runner.send_expect_ok(cmd)
        else:
            cmd = f'{port} P_RESERVATION ?'
            return self.runner.ask(cmd)

    def reset(self, port):
        """
        Reset port-level parameters to standard values, and delete all streams, filters, capture, and dataset definitions.
        :param port:
        :return:
        """
        cmd = f'{port} P_RESET'
        return self.runner.send_expect_ok(cmd)

    def info(self, port):
        """
        Multi-parameter query, obtaining all the non-settable parameters for a port.
        These parameters should not be included if the port configuration is saved and reloaded at a later time.
        :param port:
        :return:
        """
        cmd = f'{port} P_INFO ?'
        return self.runner.ask(cmd)

    def config(self, port):
        """
        Multi-parameter query, obtaining all the settable parameters for a port itself, but excluding streams,
        filters, etc.
        :param port:
        :return:
        """
        cmd = f'{port} P_CONFIG ?'
        return self.runner.ask(cmd)

    def fullconfig(self, port):
        """
        Multi-parameter query, obtaining all the settable parameters for a port itself, but excluding streams,
        filters, etc.
        :param port:
        :return:
        """
        cmd = f'{port} P_FULLCONFIG ?'
        return self.runner.ask(cmd)

    def traffic(self, port, state):
        """
        Whether a port is transmitting packets. When on, the port generates a sequence of packets with contributions
        from each stream that is enabled. The streams are configured using the PS_xxx parameters. NOTE: From Release
        57.1, if any of the specified packet sizes cannot fit into the packet generator, this command will return
        FAILED and not start the traffic.While traffic is on the streams for this port cannot be enabled or disabled,
        and the configuration of those streams that are enabled cannot be changed.
        :param port:
        :param state: coded byte, whether traffic generation is active for this port:OFF ON
        :return:
        """
        cmd = f'{port} P_TRAFFIC {state}'
        return self.runner.send_expect_ok(cmd)

    def enable_tx(self, port, state):
        """
        Whether a port should enable its transmitter, or keep the outgoing link down.
        :param port:
        :param state: onoff: coded byte, whether the transmitter is enabled. ● OFF(0) ● ON(1)
        :return:
        """
        cmd = f'{port} P_TXENABLE {state}'
        return self.runner.send_expect_ok(cmd)

    def rate(self, port):
        """
        For a port in sequential tx mode, query the port-level rate of the traffic transmitted in the manner it
        was last expressed. The response is one of P_RATEFRACTION, P_RATEPPS, or P_RATEL2BPS.
        :param port:
        :return:
        """
        cmd = f'{port} P_RATE ?'
        return self.runner.ask(cmd)

    def ratefraction(self, port, rate):
        """
        The port-level rate of the traffic transmitted for a port in sequential tx mode, expressed in millionths
        of the effective rate for the port. The bandwidth consumption includes the inter-frame gaps,
        and does not depend on the length of the packets for the streams.
        :param port:
        :param rate: integer, port rate expressed as a value between 0..1000000.
        :return:
        """
        cmd = f'{port} P_RATEFRACTION {rate}'
        return self.runner.send_expect_ok(cmd)

    def ratepps(self, port, rate):
        """
        The port-level rate of the traffic transmitted for a port in sequential tx mode,
        expressed in packets per second. The bandwidth consumption is heavily dependent on the
        length of the packets generated for the streams, and also on the inter-frame gap for the port.
        :param port:
        :param rate: integer, port rate expressed as packets per second.
        :return:
        """
        cmd = f'{port} P_RATEPPS {rate}'
        return self.runner.send_expect_ok(cmd)

    def ratel2bps(self, port, rate):
        """
        The port-level rate of the traffic transmitted for a port in sequential tx mode,
        expressed in units of bits per-second at layer-2, thus including the Ethernet header but excluding
        the inter-frame gap. The bandwidth consumption is somewhat dependent on the length of the packets
        generated for the stream, and also on the inter-frame gap for the port.
        :param port:
        :param rate: long integer, port rate expressed as bits-per-second.
        :return:
        """
        cmd = f'{port} P_RATEL2BPS {rate}'
        return self.runner.send_expect_ok(cmd)

    def macadress(self, port, mac):
        """
        A 48-bit Ethernet MAC address specified for a port.
        This address is used as the default source MAC field in the header of generated traffic for the port,
        and is also used for support of the ARP protocol..
        :param port:
        :param rate: hex bytes, specifying the six bytes of the MAC address.
        :return:
        """
        cmd = f'{port} P_MACADDRESS {mac}'
        return self.runner.send_expect_ok(cmd)

    def ipaddress(self, port, address, subnet, gateway, wild):
        """
        An IPv4 network configuration specified for a port.The address is used as the default
        source address field in the IP header of generated traffic, and the configuration is
        also used for support of the ARP and PING protocols.
        :param port:
        :param address: the IP address of the port.
        :param subnet: the subnet mask of the local network segment for the port.
        :param gateway: the gateway of the local network segment for the port.
        :param wild: wildcards used for ARP and PING replies, must be 255 or 0.
        :return:
        """
        cmd = f'{port} P_IPADDRESS {address} {subnet} {gateway} {wild}'
        return self.runner.send_expect_ok(cmd)

    def speed_selection(self, port, selection):
        """
        The speed mode for a port with an interface type supporting multiple speeds. Note:
        this is only a settable parameter for tri-speed ports. For CFP ports use the
        M_CFPCONFIG command at the module level.
        :param port:
        :param selection: coded byte, containing the speed selection for the port:
                        ● AUTO (auto-negotiate)
                        ● F10M (10 Mbps)
                        ● F100M (100 Mbps)
                        ● F1G (1000 Mbps)
                        ● F10G (10000 Mbps)
                        ● F40G (40000 Mbps)
                        ● F100G (100000 Mbps)
                        ● F10MHDX (10 Mbps half duplex)
                        ● F100MHDX (100 Mbps half duplex)
                        ● F10M100M (10/100 Mbps)
                        ● F100M1G (100/1000 Mbps)
        :return:
        """
        cmd = f'{port} P_SPEEDSELECTION {selection}'
        return self.runner.send_expect_ok(cmd)

    def brr_mode(self, port, selection):
        """
        Selects the Master/Slave setting of 100 Mbps* and 1000 Mbps** BroadR-Reach copper interfaces.
        :param port:
        :param selection:
                        ● MASTER – (default) Interface acts as a BroadR-Reach Master
                        ● SLAVE – Interface acts as a BroadR-Reach Slave
        :return:
        """
        cmd = f'{port} P_BRRMODE {selection}'
        return self.runner.send_expect_ok(cmd)

    def comment(self, port, comment):
        """
        The description of a port.
        :param port:
        :param comment: string, containing the description of the port.
        :return:
        """
        cmd = f'{port} P_COMMENT "{comment}"'
        return self.runner.send_expect_ok(cmd)

    def capture(self, port, status):
        """
        Whether a port is capturing packets. When on, the port retains the received packets and makes them available
        for inspection. The capture criterias are configured using the PC_xxxparameters.
        While capture is on the capture parameters cannot be changed.
        :param port:
        :param status: coded byte, whether capture is active for this port: OFF ON
        :return:
        """
        cmd = f'{port} P_CAPTURE {status}'
        return self.runner.send_expect_ok(cmd)

    def arpreplay(self, port, status):
        """
        Whether the port generates ping replies using the ICMP protocol.
        The port can reply to incoming ping requests to the IP address specified for the port.
        Ping reply generation is independent of whether traffic and capture is on for the port.
        :param port:
        :param status: coded byte, whether the port replies to ping requests: [ OFF | ON ]
        :return:
        """
        cmd = f'{port} P_ARPREPLY {status}'
        return self.runner.send_expect_ok(cmd)

    def pingreplay(self, port, status):
        """
        Whether the port generates replies using the Address Resolution Protocol.
        The port can reply to incoming ARP requests by mapping the IP address specified for the port
        to the MAC address specified for the port. ARP reply generation is independent
        of whether traffic and capture is on for the port.
        :param port:
        :param status: coded byte, whether the port replies to ARP requests: [ OFF | ON ]
        :return:
        """
        cmd = f'{port} P_PINGREPLY {status}'
        return self.runner.send_expect_ok(cmd)

    def trigger(self, port, start, filter1, stop, filter2):
        """
        The criteria for when to start and stop the capture process for a port.
        Even when capture is enabled with P_CAPTURE, the actual capturing of
        packets can be delayed until a particular start criteria is met by a received packet.
        Likewise, a stop criteria can be specified, based on a received packet. If no
        explicit stop criteria is specified, capture stops when the internal buffer runs full.
        In buffer overflow situations, if there is an explicit stop criteria, then the
        latest packets will be retained (and the early ones discarded), and otherwise the
        earliest packets are retained (and the later ones discarded).
        :param port:
        :param start: coded integer, the criteria for starting the actual packet capture:
                    ● ON (start immediately when capture is started)
                    ● FCSERR (start when receiving a packet containing a frame checksum error)
                    ● FILTER (start when receiving a packet satisfying a filter condition)
                    ● PLDERR (start when receiving a packet containing a packet payload error)
        :param filter1: integer, the index of a particular filter for the start criteria.
        :param stop:  coded integer, the criteria for stopping the actual packet capture:
                    ● FULL (continue until the capture buffer runs full)
                    ● FCSERR (continue until receiving a packet with a frame checksum error)
                    ● FILTER (continue until receiving a packet satisfying a filter condition)
                    ● PLDERR (continue until receiving a packet with a packet payload error)
                    ● USERSTOP* (continue until the user stops the capture manually)
        :param filter2:  integer, the index of a particular filter for the stop criteria.
        :return:
        """
        cmd = f'{port} PC_TRIGGER {start} {filter1} {stop} {filter2}'
        return self.runner.send_expect_ok(cmd)

    def keep(self, port, which, index, bytes):
        """
        Which packets to keep once the start criteria has been triggered for a port.
        Also how big a portion of each packet to retain, saving space for more packets in the capture buffer.
        :param port:
        :param which: coded integer, which general kind of packets to keep:
                    ● ALL (keep all packets between the start and stop trigger)
                    ● FCSERR (keep only those packets with frame checksum errors)
                    ● NOTPLD (keep only those packets without a test payload)
                    ● TPLD (keep only those packets with a test payload and specific id)
                    ● FILTER (keep only those packets satisfying a specific filter condition)
                    ● PLDERR (Keep only those packets with payload errors)
        :param index: integer, test payload id or filter index for which packets to keep.
        :param bytes: integer, how many bytes to keep in the buffer for of each packet.
                    The value -1 means no limit on packet size.
        :return:
        """
        cmd = f'{port} PC_KEEP {which} {index} {bytes}'
        return self.runner.send_expect_ok(cmd)

    def packet(self, port, cid):
        """
        Obtains the raw bytes of a captured packet for a port. The packet data may be truncated if
        the PC_KEEP parameter specified a limit on the number of bytes kept.
        :param port:
        :param cid: integer, the sub-index value of the captured packet.
            hexdata: hex bytes, the raw bytes kept for the packet.
        :return:
        """
        cmd = f'{port} PC_PACKET [{cid}] ?'
        return self.runner.ask(cmd)

    def stats(self, port):
        """
        Obtains the number of packets currently in the capture buffer for a port.
        The count is reset to zero when capture is turned on.
        Example 0/1 PC_STATS 0 987 3453543453
        status: long integer, 1 if capture has been stopped because of overflow, 0 if still running..
        packets: long integer, the number of packets in the buffer.
        starttime: long integer, time when capture was started, in nano-seconds since 2010-01-01.
        :param port:
        :return:
        """
        cmd = f'{port} PC_STATS ?'
        return self.runner.ask(cmd)

    def pt_clear(self, port):
        """
        Clear all the transmit statistics for a port. The byte and packet counts will restart at zero.
        :param port:
        :return:
        """
        cmd = f'{port} PT_CLEAR'
        return self.runner.send_expect_ok(cmd)

    def pr_clear(self, port):
        """
        Clear all the receive statistics for a port. The byte and packet counts will restart at zero.
        :param port:
        :return:
        """
        cmd = f'{port} PR_CLEAR'
        return self.runner.send_expect_ok(cmd)
