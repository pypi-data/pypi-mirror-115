# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 14:54
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : stream.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 :
# ----------------------------------------------------------------

from .runner import Runner


class Stream:

    def __init__(self, runner: Runner):
        self.runner = runner

    def indices(self, port):
        """
        The full list of which streams are defined for a port. These are the sub-index values that are used
        for the parameters defining the traffic patterns transmitted for the port.
        Setting the value of this parameter creates a new empty stream for each value that is not already in use,
        and deletes each stream that is not mentioned in the list.
        The same can be accomplished one-stream-at-a-time using the PS_CREATE and PS_DELETE commands.
        :param port:
        :return:
        """
        cmd = f'{port} PS_INDICES ?'
        return self.runner.ask(cmd)

    def create(self, port, sid):
        """
        Creates an empty stream definition with the specified sub-index value.
        :param port:
        :param sid: integer, the sub-index value of the stream definition to create.
        :return:
        """
        cmd = f'{port} PS_CREATE [{sid}]'
        return self.runner.send_expect_ok(cmd)

    def delete(self, port, sid):
        """
        Deletes the stream definition with the specified sub-index value.
        :param port:
        :param sid: the sub-index value of the stream definition to delete.
        :return:
        """
        cmd = f'{port} PS_DELETE [{sid}]'
        return self.runner.send_expect_ok(cmd)

    def enable(self, port, sid, state):
        """
        This property determines if a stream contributes outgoing packets for a port. The value can be toggled between
        ON and SUPPRESS while traffic is enabled at the port level. Streams in the OFF state cannot be set to any
        other value while traffic is enabled.
        The sum of the rates of all enabled or suppressed streams must not exceed the effective port rate.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :param state: coded integer, specifies the state of the stream:
                    ● OFF (0) (stream will not be used when port traffic is started)
                    ● ON (1) (stream will be started when port traffic is started)
                    ● SUPPRESS (2) (stream will not be started when port traffic is started but can be started afterwards)
        :return:
        """
        cmd = f'{port} PS_ENABLE [{sid}] {state}'
        return self.runner.send_expect_ok(cmd)

    def comment(self, port, sid, comment):
        """
        The description of a stream.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :param comment: string, containing the description of the stream.
        :return:
        """
        cmd = f'{port} PS_COMMENT [{sid}] "{comment}"'
        return self.runner.send_expect_ok(cmd)

    def set_insertfcs(self, port, sid, state):
        """
        Whether a valid frame checksum is added to the packets of a stream.
        :param port:
        :param sid: integer, the sub-index value of the stream definition
        :param state: coded integer, whether frame checksums are inserted: OFF, ON
        :return:
        """
        cmd = f'{port} PS_INSERTFCS [{sid}] {state}'
        return self.runner.send_expect_ok(cmd)

    def set_tpldid(self, port, sid, tpldid):
        """
        The identifier of the test payloads inserted into packets transmitted for a stream.
        A value of -1 disables test payloads for the stream. Test payloads are inserted at the end of each packet,
        and contains time-stamp and sequence-number information. This allows the receiving port to provide
        error-checking and latency measurements, in addition to the basic counts and rate measurements provided
        for all traffic. The test payload identifier furthermore allows the receiving port to distinguish multiple
        different streams, which may originate from multiple different chassis. Since test payloads are an inter-port
        and inter-chassis mechanism, the test payload identifier assignments should be planned globally across all
        the chassis and ports of the testbed.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :param tpldid: integer, the test payload identifier value.
                    -1 (disable test payloads)
        :return:
        """
        cmd = f'{port} PS_TPLDID [{sid}] {tpldid}'
        return self.runner.send_expect_ok(cmd)

    def set_header_protocol(self, port, sid, *args):
        """
        This parameter will inform the Xena tester how to interpret the packet header byte sequence specified with
        PS_PACKETHEADER. This is mainly for information purposes, and the stream will transmit the packet header bytes
        even if no protocol segments are specified. The Xena tester however support calculation of certain field values
        in hardware, such as the IP, TCP and UDP length and checksum fields. This allow the use of hardware modifiers
        for these protocol segments. In order for this function to work the Xena tester needs to know the type of each
        segment that precedes the segment where the hardware calculation is to be performed. Refer to this page for
        more details on hardware-based calculation of protocol fields.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :param args: coded integer, a number specifying a built-in protocol segment:
                    ● ETHERNET (14 bytes)
                    ● VLAN (4 bytes)
                    ● ARP (28 bytes)
                    ● IP (20 bytes)
                    ● IPV6 (40 bytes)
                    ● UDP (8 bytes)
                    ● TCP (20 bytes)
                    ● LLC (3 bytes)
                    ● SNAP (5 bytes)
                    ● GTP (20 bytes)
                    ● ICMP (8 bytes)
                    ● RTP (12 bytes)
                    ● RTCP (4 bytes)
                    ● STP (35 bytes)
                    ● SCTP (12 bytes)
                    ● MACCTRL (4 bytes)
                    ● MPLS (4 bytes)
                    ● PBBTAG (4 bytes)
                    ● FCOE (14 bytes)
                    ● FC (24 bytes)
                    ● FCOETAIL > > (4 bytes) 94
                    ● IGMP0 (12 bytes)
                    ● IGMP1 (16 bytes)
                    ● -n (n bytes raw segment)
        :return:
        """
        cmd = f'{port} PS_HEADERPROTOCOL [{sid}]'
        for segment in args:
            cmd += f' {segment}'
        return self.runner.send_expect_ok(cmd)

    def set_rate_fraction(self, port, sid, fraction):
        """
        The rate of the traffic transmitted for a stream, expressed in millionths of the effective rate for the port.
        The bandwidth consumption includes the inter-frame gap, and is independent of the length of the packets
        generated for the stream. The sum of the bandwidth consumption for all the enabled streams must not exceed
        the effective rate for the port.
        Setting this parameter also instructs the Manager to attempt to keep the rate-percentage unchanged in case it
        has to cap stream rates. Getting it is only valid if the rate was last set using this parameter.
        :param port:
        :param sid: integer,the sub-index value of the stream definition
        :param fraction: integer, stream rate expressed as a value between 0..1000000.
        :return:
        """
        cmd = f'{port} PS_RATEFRACTION [{sid}] {fraction}'
        return self.runner.send_expect_ok(cmd)

    def set_packet_header(self, port, sid, hexdata):
        """
        The first portion of the packet bytes that are transmitted for a stream. This starts with the 14 bytes of
        the Ethernet header, followed by any contained protocol segments. All packets transmitted for the
        stream start with this fixed header. Individual byte positions of the packet header may be varied on a
        packet-to-packet basis using modifiers. The full packet comprises the header, the payload, an optional test
        payload, and the frame checksum. The header data is specified as raw bytes, since the script environment
        does not know the field-by-field layout of the various protocol segments. But XenaManager does, so in practice
        you may use XenaManager’s packet editor, and simply query for the resulting hex string at the script level.
        :param port:
        :param sid: integer, the sub-index value of the stream definition. hexdata: hex bytes, the raw bytes
                    comprising the packet header.
        :param hexdata:
        :return:
        """
        cmd = f'{port} PS_PACKETHEADER [{sid}] {hexdata}'
        return self.runner.send_expect_ok(cmd)

    def set_arp_request(self, port, sid, macaddress):
        """
        Generates an outgoing ARP request on the test port.
        The packet header for the stream must contain an IP protocol segment, and the
        destination IP address is used in the ARP request. If there is a gateway IP address
        specified for the port and it is on a different subnet than the destination IP address
        in the packet header, then the gateway IP address is used instead.
        The framing of the ARP request matches the packet header, including any VLAN
        protocol segments.
        This script parameter does not generate an immediate result, but waits until an ARP
        reply is received on the test port. If no reply is received within 500 milliseconds, it
        returns <FAILED>.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :param macaddress: hex bytes, specifying the six bytes of the MAC address.
        :return:
        """
        cmd = f'{port} PS_ARPREQUEST [{sid}] {macaddress}'
        return self.runner.send_expect_ok(cmd)

    def set_packet_length(self, port, sid, min, max, _type):
        """
        The length distribution of the packets transmitted for a stream.
        The length of the packets transmitted for a stream can be varied from packet to
        packet, according to a choice of distributions within a specified min..max range.
        The length of each packet is reflected in the size of the payload portion of the
        packet, whereas the header has constant length.
        Length variation complements, and is independent of, the content variation
        produced by header modifiers.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :param min: integer, lower limit on the packet length.
        :param max: integer, upper limit on the packet length.
        :param _type: coded integer, the kind of distribution:
                        ● FIXED (all packets have min size)
                        ● INCREMENTING (incrementing from min to max)
                        ● BUTTERFLY (min, max, min+1, max-1, min+2, max-2, etc)
                        ● RANDOM (random between min and max)
                        ● MIX (a mixture of sizes between 56 and 1518, average 464 bytes)
        :return:
        """
        cmd = f'{port} PS_PACKETLENGTH [{sid}] {_type} {min} {max}'
        return self.runner.send_expect_ok(cmd)

    def set_payload(self, port, sid, hexdata, _type):
        """
        The payload content of the packets transmitted for a stream.
        The payload portion of a packet starts after the header and continues up until the
        test payload or the frame checksum. The payload may vary in length, and is filled
        with either an incrementing sequence of byte values, or a repeated multi-byte
        pattern.
        Length variation complements, and is independent of, the content variation
        produced by header modifiers.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :param hexdata: hex bytes, a pattern of bytes to be repeated. The maximum length of the pattern is
                        18 bytes. Only used if type is set to PATTERN.
        :param _type: coded integer, the kind of payload content:
                    ● PATTERN (a pattern is repeated up through the packet)
                    ● INCREMENTING (bytes are incremented up through the packet)
                    ● PRBS (bytes are randomized from packet to packet)
                    ● RANDOM (a random generated pattern)
        :return:
        """
        cmd = f'{port} PS_PAYLOAD [{sid}] {_type} {hexdata}'
        return self.runner.send_expect_ok(cmd)

    def set_packetlimit(self, port, sid, limit):
        """
        Based on different port transmission mode, the meaning of this API is different.
        When Port TX Mode is set to NORMAL, STRICT UNIFORM or BURST*: The number of packets that will be
        transmitted when traffic is started on a port. A value of 0 or -1 makes the stream transmit continuously.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :param limit: integer, the number of packets. 0 or -1 (disable packet limitation)
        :return:
        """
        cmd = f'{port} PS_PACKETLIMIT [{sid}] {limit}'
        return self.runner.send_expect_ok(cmd)

    def arp_request(self, port, sid):
        """
        Generates an outgoing ARP request on the test port.
        The packet header for the stream must contain an IP protocol segment,
        and the destination IP address is used in the ARP request.
        If there is a gateway IP address specified for the port and it is on a different
        subnet than the destination IP address in the packet header, then the gateway IP address
        is used instead. The framing of the ARP request matches the packet header,
        including any VLAN protocol segments.
        This script parameter does not generate an immediate result,
        but waits until an ARP reply is received on the test port.
        If no reply is received within 500 milliseconds, it returns <FAILED>.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :return:
        """
        cmd = f'{port} PS_ARPREQUEST [{sid}] ?'
        return self.runner.ask(cmd, 1)

    def ping_request(self, port, sid):
        """
        Generates an outgoing ping request using the ICMP protocol on the test port.
        The packet header for the stream must contain an IP protocol segment, with valid source and
        destination IP addresses. The framing of the ping request matches the packet header,
        including any VLAN protocol segments, and the destination MAC address must also be valid,
        possibly containing a value obtained with PS_ARPREQUEST. This script parameter does
        not generate an immediate result, but waits until a ping reply is received on the test port.
        If no reply is received within 2000 milliseconds, it returns <FAILED>.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :return:
        """
        cmd = f'{port} PS_PINGREQUEST [{sid}] ?'
        return self.runner.ask(cmd, 2)

    def set_ipv4gateway(self, port, sid, ipv4_gateway):
        cmd = f'{port} PS_IPV4GATEWAY [{sid}] {ipv4_gateway}'
        return self.runner.send_expect_ok(cmd)

    def get_fullconfig(self, port):
        """
        Multi-parameter query, obtaining all parameters for all streams defined on a port.
        :param port:
        :return:
        """
        cmd = f'{port} PS_FULLCONFIG ?'
        return self.runner.ask(cmd)

    def config(self, port, sid):
        """
        Multi-parameter query, obtaining all the parameters for a specific stream.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :return:
        """
        cmd = f'{port} PS_CONFIG  [{sid}] ?'
        return self.runner.ask(cmd)

    def set_ratepps(self, port, sid, rate):
        """
        The rate of the traffic transmitted for a stream, expressed in packets per second.
        The bandwidth consumption is heavily dependent on the length of the packets generated for the stream,
        and also on the inter-frame gap for the port. The sum of the bandwidth consumption for all the
        enabled streams must not exceed the effective rate for the port.
        Setting this parameter also instructs the Manager to attempt to keep the packets-per-second
        unchanged in case it has to cap stream rates.
        Getting it is only valid if the rate was last set using this parameter. sid: integer,
        the sub-index value of the stream definition.
        :param port:
        :param sid:
        :param rate: stream rate expressed as packets per second.
        :return:
        """
        cmd = f'{port} PS_RATEPPS [{sid}] {rate}'
        return self.runner.send_expect_ok(cmd)

    def set_ratel2bps(self, port, sid, rate):
        """
        The rate of the traffic transmitted for a stream, expressed in units of bits-per-second at layer-2,
        thus including the Ethernet header but excluding the inter-frame gap.
        The bandwidth consumption is somewhat dependent on the length of the packets generated for the stream,
        and also on the inter-frame gap for the port.
        The sum of the bandwidth consumption for all the enabled streams must not exceed the
        effective rate for the port. Setting this parameter also instructs the Manager to attempt to keep
        the layer-2 bps rate unchanged in case it has to cap stream rates. Getting it is only valid if
        the rate was last set using this parameter.
        :param port:
        :param sid:
        :param rate: stream rate expressed as bits-per-second.
        :return:
        """
        cmd = f'{port} PS_RATEL2BPS [{sid}] {rate}'
        return self.runner.send_expect_ok(cmd)

    def get_stream(self, port, sid):
        """
        PT_STREAM [sid] bps pps bytes packets

        Obtains statistics concerning the packets of a specific stream transmitted on a port.

        Data Values
            bps: long integer, number of bits transmitted in the last second.
            pps: long integer, number of packets transmitted in the last second.
            bytes: long integer, number of bytes transmitted since statistics were cleared.
            packets: long integer, number of packets transmitted since statistics were cleared.
        :param port:
        :param sid: integer, the sub-index value of the stream definition.
        :return:
        """
        cmd = f'{port} PT_STREAM [{sid}] ?'
        return self.runner.ask(cmd)

    def get_tpldtraffic(self, port, tid):
        """
        PR_TPLDTRAFFIC [tid] bps pps byt pac

        Obtains traffic statistics concerning the packets with a particular test payload id received on a port.

        Data Values
            tid: integer, the identifier of the test payload.
            bps: long integer, number of bits received in the last second.
            pps: long integer, number of packets received in the last second.
            byt: long integer, number of bytes received since statistics were cleared.
            pac: long integer, number of packets received since statistics were cleared.
        :param port:
        :param tid: integer, the identifier of the test payload.
        :return:
        """
        cmd = f'{port} PR_TPLDTRAFFIC [{tid}] ?'
        return self.runner.ask(cmd)

    def get_tpldlatency(self, port, tid):
        """
        PR_TPLDLATENCY [tid] min avg max avg1sec min1sec max1sec

        Obtains statistics concerning the latency experienced by the packets with a particular test payload id
        received on a port. The values are adjusted by the port-level P_LATENCYOFFSET value.
        A special value of -1 is returned if latency numbers are not applicable.
        Latency is only meaningful when the clocks of the transmitter and receiver are synchronized. This requires
        the two ports to be on the same test module, and it requires knowledge of the global test environment to
        ensure that packets are in fact routed between these ports.

        Data Values
            tid: integer, the identifier of the test payload
            min: long integer, nanoseconds, minimum latency for test payload stream
            avg: long integer, nanoseconds, average latency for test payload stream
            max: long integer, nanoseconds, maximum latency for test payload stream
            avg1sec: long integer, nanoseconds, average latency over last 1-second period
            min1sec*: long integer, nanoseconds, minimum latency during last 1-second period

        :param port:
        :param tid: integer, the identifier of the test payload
        :return:
        """
        cmd = f'{port} PR_TPLDLATENCY [{tid}] ?'
        return self.runner.ask(cmd)

    def get_tplderrors(self, port, tid):
        """
        PR_TPLDERRORS [tid] dummy seq mis pld

        Obtains statistics concerning errors in the packets with a particular test payload id received on a port.
        The error information is derived from analysing the various fields contained in the embedded test payloads of
        the received packets, independent of which chassis and port may have originated the packets.
        Note that packet-lost statistics involve both a transmitting port and a receiving port, and in particular
        knowing which port originated the packets with a particular test payload identifier. This information requires
        knowledge of the global test environment, and is not supported at the port-level.

        Data Values
            dummy: long integer, not used
            seq: long integer, number of non-incrementing-sequence-number events.
            mis: long integer, number of swapped-sequence-number misorder events.
            pld: long integer, number of packets with non-incrementing payload content.

        :param port:
        :param tid:  integer, the identifier of the test payload
        :return:
        """
        cmd = f'{port} PR_TPLDERRORS [{tid}] ?'
        return self.runner.ask(cmd)

    def get_extra(self, port, *args):
        """
        PR_EXTRA miscstats…

        Obtains statistics concerning special packets received on a port since receive statistics were cleared.

        Parameters
            fcserrors: long integer, number of packets with frame checksum errors.
            pauseframes: long integer, number of Ethernet pause frames.
            arprequests: long integer, number of ARP request packets received.
            arpreplies: long integer, number of ARP reply packets received.
            pingrequests: long integer, number of PING request packets received.
            pingreplies: long integer, number of PING reply packets received.
            gapcount: long integer, number of gap monitor gaps encountered.
            gapduration: long integer, combined duration of gap monitor gaps encountered, microseconds.

        :param port:
        :param args:
        :return:
        """
        cmd = f'{port} PR_EXTRA'
        for parameter in args:
            cmd += f' {parameter}'
        cmd += ' ?'
        return self.runner.ask(cmd)
