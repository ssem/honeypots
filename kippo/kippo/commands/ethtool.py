from kippo.core.honeypot import HoneyPotCommand
from twisted.internet import reactor

commands = {}

class command_ethtool(HoneyPotCommand):
    def start(self):
        if '--help' in self.args or '-h' in self.args:
            self.help()
            self.exit()
            return
        elif '--version' in self.args:
            self.writeln('ethtool version 3.13')
            self.exit()
            return

        iface = ''
        if 'eth0' in self.args:
            iface = 'eth0'
        elif 'lo' in self.args:
            iface = 'lo'

        if iface == '':
             for l in (
                'ethtool: bad command line argument(s)',
                'For more information run ethtool -h',
                ):
                self.writeln(l)
        elif '-a' in self.args:
            for l in (
                'Pause parameters for %s:' % iface,
                'Cannot get device pause settings: Operation not supported',
                ):
                self.writeln(l)
        elif '-A' in self.args:
            self.writeln('Cannot get device pause settings: Operation not supported')
        elif '-c' in self.args:
            for l in (
               'Coalesce parameters for eth0:',
                'Cannot get device coalesce settings: Operation not supported',
                ):
                self.writeln(l)
        elif '-C' in self.args:
            self.writeln('Cannot get device coalesce settings: Operation not supported')
        elif '-g' in self.args:
            for l in (
                'Ring parameters for %s:' % iface,
                'Pre-set maximums:',
                'RX:             256',
                'RX Mini:        0',
                'RX Jumbo:       0',
                'TX:             256',
                'Current hardware settings:',
                'RX:             256',
                'RX Mini:        0',
                'RX Jumbo:       0',
                'TX:             256',
                ):
                self.writeln(l)
        elif '-G' in self.args:
            self.writeln('Cannot get device ring settings: Operation not supported')
        elif '-i' in self.args:
            for l in (
                'driver: virtio_net',
                'version: 1.0.0',
                'firmware-version:',
                'bus-info: 0000:00:03.0',
                'supports-statistics: no',
                'supports-test: no',
                'supports-eeprom-access: no',
                'supports-register-dump: no',
                'supports-priv-flags: no',
                ):
                self.writeln(l)
        elif '-d' in self.args or '-e' in self.args or '-E' in self.args:
            self.writeln('Cannot get driver information: Operation not supported')
        elif '-k' in self.args:
            for l in (
                'Features for %s:' % iface,
                'rx-checksumming: on [fixed]',
                'tx-checksumming: on',
                '    tx-checksum-ipv4: off [fixed]',
                '    tx-checksum-ip-generic: on [fixed]',
                '    tx-checksum-ipv6: off [fixed]',
                '    tx-checksum-fcoe-crc: off [fixed]',
                '    tx-checksum-sctp: off [fixed]',
                'scatter-gather: on',
                '    tx-scatter-gather: on [fixed]',
                '    tx-scatter-gather-fraglist: on [fixed]',
                'tcp-segmentation-offload: on',
                '    tx-tcp-segmentation: on',
                '    tx-tcp-ecn-segmentation: on',
                '    tx-tcp6-segmentation: on',
                'udp-fragmentation-offload: on',
                'generic-segmentation-offload: on',
                'generic-receive-offload: on',
                'large-receive-offload: off [fixed]',
                'rx-vlan-offload: off [fixed]',
                'tx-vlan-offload: off [fixed]',
                'ntuple-filters: off [fixed]',
                'receive-hashing: off [fixed]',
                'highdma: on [fixed]',
                'rx-vlan-filter: off [fixed]',
                'vlan-challenged: on [fixed]',
                'tx-lockless: on [fixed]',
                'netns-local: on [fixed]',
                'tx-gso-robust: off [fixed]',
                'tx-fcoe-segmentation: off [fixed]',
                'tx-gre-segmentation: off [fixed]',
                'tx-ipip-segmentation: off [fixed]',
                'tx-sit-segmentation: off [fixed]',
                'tx-udp_tnl-segmentation: off [fixed]',
                'tx-mpls-segmentation: off [fixed]',
                'fcoe-mtu: off [fixed]',
                'tx-nocache-copy: off [fixed],'
                'loopback: on [fixed]',
                'rx-fcs: off [fixed]',
                'rx-all: off [fixed]',
                'tx-vlan-stag-hw-insert: off [fixed]',
                'rx-vlan-stag-hw-parse: off [fixed]',
                'rx-vlan-stag-filter: off [fixed]',
                'l2-fwd-offload: off [fixed]',
                ):
                self.writeln(l)
        elif '-K' in self.args:
            self.writeln('no features changed')
        elif '-p' in self.args:
            self.writeln('Cannot identify NIC: Operation not supported')
        elif '-P' in self.args:
            self.writeln('Permanent address: 00:00:00:00:00:00')
        elif '-r' in self.args:
            self.writeln('Cannot restart autonegotiation: Operation not supported')
        elif '-S' in self.args:
            self.writeln('no stats available')
        elif '-t' in self.args:
            self.writeln('Cannot test: Operation not supported')
        elif '-s' in self.args:
            pass
        elif '-n' in self.args:
            for l in (
                'Cannot get RX rings: Operation not supported',
                'rxclass: Cannot get RX class rule count: Operation not supported',
                'RX classification rule retrieval failed',
                ):
                self.writeln(l)
        elif '-w' in self.args:
            for l in (
                'Can not get dump level',
                ': Operation not supported',
                ):
                self.writeln(l)
        elif '-T' in self.args:
            for l in (
                'Time stamping parameters for %s:' % iface,
                'Capabilities:',
                '    software-receive      (SOF_TIMESTAMPING_RX_SOFTWARE)',
                '    software-system-clock (SOF_TIMESTAMPING_SOFTWARE)',
                'PTP Hardware Clock: none',
                'Hardware Transmit Timestamp Modes: none',
                'Hardware Receive Filter Modes: none',
                ):
                self.writeln(l)
        elif '-x' in self.args:
            self.writeln('Cannot get RX ring count: Operation not supported')
        elif '-l' in self.args:
            for l in (
                'Channel parameters for lo:',
                'Cannot get device channel parameters',
                ': Operation not supported',
                ):
                self.writeln(l)
        elif '-L' in self.args:
            self.writeln('Cannot get device channel parameters: Operation not supported')
        elif '-m' in self.args:
            self.writeln('Cannot get module EEPROM information: Operation not supported')
        else:
            for l in (
                'Settings for %s:' % iface,
                '\tLink detected: yes',
                ):
                self.writeln(l)
        self.exit()
        return

    def help(self):
        for l in (
            'ethtool version 3.13',
            'Usage:',
            '        ethtool DEVNAME Display standard information about device',
            '        ethtool -s|--change DEVNAME     Change generic options',
            '        [ speed %d ]',
            '        [ duplex half|full ]',
            '        [ port tp|aui|bnc|mii|fibre ]',
            '        [ mdix auto|on|off ]',
            '        [ autoneg on|off ]',
            '        [ advertise %x ]',
            '        [ phyad %d ]',
            '        [ xcvr internal|external ]',
            '        [ wol p|u|m|b|a|g|s|d... ]',
            '        [ sopass %x:%x:%x:%x:%x:%x ]',
            '        [ msglvl %d | msglvl type on|off ... ]',
            '        ethtool -a|--show-pause DEVNAME Show pause options',
            '        ethtool -A|--pause DEVNAME      Set pause options',
            '        [ autoneg on|off ]',
            '        [ rx on|off ]',
            '        [ tx on|off ]',
            '        ethtool -c|--show-coalesce DEVNAME      Show coalesce options',
            '        ethtool -C|--coalesce DEVNAME   Set coalesce options',
            '        [adaptive-rx on|off]',
            '        [adaptive-tx on|off]',
            '        [rx-usecs N]',
            '        [rx-frames N]',
            '        [rx-usecs-irq N]',
            '        [rx-frames-irq N]',
            '        [tx-usecs N]',
            '        [tx-frames N]',
            '        [tx-usecs-irq N]',
            '        [tx-frames-irq N]',
            '        [stats-block-usecs N]',
            '        [pkt-rate-low N]',
            '        [rx-usecs-low N]',
            '        [rx-frames-low N]',
            '        [tx-usecs-low N]',
            '        [tx-frames-low N]',
            '        [pkt-rate-high N]',
            '        [rx-usecs-high N]',
            '        [rx-frames-high N]',
            '        [tx-usecs-high N]',
            '        [tx-frames-high N]',
            '        [sample-interval N]',
            '        ethtool -g|--show-ring DEVNAME  Query RX/TX ring parameters',
            '        ethtool -G|--set-ring DEVNAME   Set RX/TX ring parameters',
            '        [ rx N ]',
            '        [ rx-mini N ]',
            '        [ rx-jumbo N ]',
            '        [ tx N ]',
            '        ethtool -k|--show-features|--show-offload DEVNAME       Get state of protocol offload and other features',
            '        ethtool -K|--features|--offload DEVNAME Set protocol offload and other features',
            '        FEATURE on|off ...',
            '        ethtool -i|--driver DEVNAME     Show driver information',
            '        ethtool -d|--register-dump DEVNAME      Do a register dump',
            '        [ raw on|off ]',
            '        [ file FILENAME ]',
            '        ethtool -e|--eeprom-dump DEVNAME        Do a EEPROM dump',
            '        [ raw on|off ]',
            '        [ offset N ]',
            '        [ length N ]',
            '        ethtool -E|--change-eeprom DEVNAME      Change bytes in device EEPROM',
            '        [ magic N ]',
            '        [ offset N ]',
            '        [ length N ]',
            '        [ value N ]',
            '        ethtool -r|--negotiate DEVNAME  Restart N-WAY negotiation',
            '        ethtool -p|--identify DEVNAME   Show visible port identification (e.g. blinking)',
            '               [ TIME-IN-SECONDS ]',
            '        ethtool -t|--test DEVNAME       Execute adapter self test',
            '               [ online | offline | external_lb ]',
            '        ethtool -S|--statistics DEVNAME Show adapter statistics',
            '        ethtool -n|-u|--show-nfc|--show-ntuple DEVNAME  Show Rx network flow classification options or rules',
            '        [ rx-flow-hash tcp4|udp4|ah4|esp4|sctp4|tcp6|udp6|ah6|esp6|sctp6 |',
            '          rule %d ]',
            '        ethtool -N|-U|--config-nfc|--config-ntuple DEVNAME      Configure Rx network flow classification options or rules',
            '        rx-flow-hash tcp4|udp4|ah4|esp4|sctp4|tcp6|udp6|ah6|esp6|sctp6 m|v|t|s|d|f|n|r... |',
            '        flow-type ether|ip4|tcp4|udp4|sctp4|ah4|esp4',
            '            [ src %x:%x:%x:%x:%x:%x [m %x:%x:%x:%x:%x:%x] ]',
            '            [ dst %x:%x:%x:%x:%x:%x [m %x:%x:%x:%x:%x:%x] ]',
            '            [ proto %d [m %x] ]',
            '            [ src-ip %d.%d.%d.%d [m %d.%d.%d.%d] ]',
            '            [ dst-ip %d.%d.%d.%d [m %d.%d.%d.%d] ]',
            '            [ tos %d [m %x] ]',
            '            [ l4proto %d [m %x] ]',
            '            [ src-port %d [m %x] ]',
            '            [ dst-port %d [m %x] ]',
            '            [ spi %d [m %x] ]',
            '            [ vlan-etype %x [m %x] ]',
            '            [ vlan %x [m %x] ]',
            '            [ user-def %x [m %x] ]',
            '            [ dst-mac %x:%x:%x:%x:%x:%x [m %x:%x:%x:%x:%x:%x] ]',
            '            [ action %d ]',
            '            [ loc %d]] |',
            '        delete %d',
            '        ethtool -T|--show-time-stamping DEVNAME Show time stamping capabilities',
            '        ethtool -x|--show-rxfh-indir DEVNAME    Show Rx flow hash indirection',
            '        ethtool -X|--set-rxfh-indir DEVNAME     Set Rx flow hash indirection',
            '        equal N | weight W0 W1 ...',
            '        ethtool -f|--flash DEVNAME      Flash firmware image from the specified file to a region on the device',
            '               FILENAME [ REGION-NUMBER-TO-FLASH ]',
            '        ethtool -P|--show-permaddr DEVNAME      Show permanent hardware address',
            '        ethtool -w|--get-dump DEVNAME   Get dump flag, data',
            '        [ data FILENAME ]',
            '        ethtool -W|--set-dump DEVNAME   Set dump flag of the device',
            '        N',
            '        ethtool -l|--show-channels DEVNAME      Query Channels',
            '        ethtool -L|--set-channels DEVNAME       Set Channels',
            '               [ rx N ]',
            '               [ tx N ]',
            '               [ other N ]',
            '               [ combined N ]',
            '        ethtool --show-priv-flags DEVNAME       Query private flags',
            '        ethtool --set-priv-flags DEVNAME        Set private flags',
            '        FLAG on|off ...',
            '        ethtool -m|--dump-module-eeprom|--module-info DEVNAME   Query/Decode Module EEPROM information and optical diagnostics if available',
            '        [ raw on|off ]',
            '        [ hex on|off ]',
            '        [ offset N ]',
            '        [ length N ]',
            '        ethtool --show-eee DEVNAME      Show EEE settings',
            '        ethtool --set-eee DEVNAME       Set EEE settings',
            '        [ eee on|off ]',
            '        [ advertise %x ]',
            '        [ tx-lpi on|off ]',
            '        [ tx-timer %d ]',
            '        ethtool -h|--help               Show this help',
            '        ethtool --version               Show version number',
            ):
            self.writeln(l)

commands['/sbin/ethtool'] = command_ethtool
