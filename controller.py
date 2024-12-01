from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

class Controller:

    def __init__(self):
        self.topo = load_topo("topology.json")
        self.controllers = {}
        self.connect_to_devices()
        self.program_devices()

    def connect_to_devices(self):
        for sw_name in self.topo.get_p4switches():
            thrift_port = self.topo.get_thrift_port(sw_name)
            self.controllers[sw_name] = SimpleSwitchThriftAPI(thrift_port)

    def program_devices(self):
        self.program_router('r1')
        self.program_router('r2')

        self.program_switch('s1')
        self.program_switch('s2')
        self.program_switch('s3')
        self.program_switch('s4')

    def program_router(self, router_name):
        controller = self.controllers[router_name]
        if router_name == 'r1':
            controller.table_add("routing_table", "ipv4_forward", ["10.0.1.0/24", "0x00"], ["10.0.1.1", "2"]) # default best effort queue (queue 4)
            controller.table_add("routing_table", "ipv4_forward", ["10.0.1.0/24", "0x2E"], ["10.0.1.1", "2"]) # same route (queue 1)
            controller.table_add("routing_table", "ipv4_forward", ["10.0.1.0/24", "0x18"], ["10.0.1.1", "2"]) # same route (queue 2)
            controller.table_add("routing_table", "ipv4_forward", ["10.0.1.0/24", "0x14"], ["10.0.1.1", "2"]) # same route (queue 3)

            controller.table_add("routing_table", "ipv4_forward", ["10.0.2.0/24", "0x00"], ["10.0.2.1", "3"])
            controller.table_add("routing_table", "ipv4_forward", ["10.0.3.0/24", "0x00"], ["192.168.1.2", "1"])
            controller.table_add("routing_table", "ipv4_forward", ["10.0.4.0/24", "0x00"], ["192.168.1.2", "1"])

            controller.table_add("switching_table", "set_dmac", ["10.0.1.1"], ["00:00:00:00:01:01"])
            controller.table_add("switching_table", "set_dmac", ["10.0.2.1"], ["00:00:00:00:02:01"])
            controller.table_add("switching_table", "set_dmac", ["192.168.1.2"], ["00:00:00:00:06:01"])


            controller.table_add("mac_rewriting_table", "set_smac", ["1"], ["00:00:00:00:05:01"])
            controller.table_add("mac_rewriting_table", "set_smac", ["2"], ["00:00:00:00:05:02"])
            controller.table_add("mac_rewriting_table", "set_smac", ["3"], ["00:00:00:00:05:03"])

        elif router_name == 'r2':
            controller.table_add("routing_table", "ipv4_forward", ["10.0.3.0/24", "0x00"], ["10.0.3.1", "2"])
            controller.table_add("routing_table", "ipv4_forward", ["10.0.4.0/24", "0x00"], ["10.0.4.1", "3"])
            controller.table_add("routing_table", "ipv4_forward", ["10.0.1.0/24", "0x00"], ["192.168.1.1", "1"])
            controller.table_add("routing_table", "ipv4_forward", ["10.0.2.0/24", "0x00"], ["192.168.1.1", "1"])

            controller.table_add("switching_table", "set_dmac", ["10.0.3.1"], ["00:00:00:00:03:01"])
            controller.table_add("switching_table", "set_dmac", ["10.0.4.1"], ["00:00:00:00:04:01"])
            controller.table_add("switching_table", "set_dmac", ["192.168.1.1"], ["00:00:00:00:05:01"])


            controller.table_add("mac_rewriting_table", "set_smac", ["1"], ["00:00:00:00:06:01"])
            controller.table_add("mac_rewriting_table", "set_smac", ["2"], ["00:00:00:00:06:02"])
            controller.table_add("mac_rewriting_table", "set_smac", ["3"], ["00:00:00:00:06:03"])

    def program_switch(self, switch_name):
        controller = self.controllers[switch_name]
        if switch_name == 's1':
            controller.table_set_default("ipv4_lpm", "drop")
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.1.10/32"], ["00:00:0a:00:01:01", "2"])
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.1.20/32"], ["00:00:0a:00:01:02", "3"])
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.0.0/16"], ["00:00:00:00:05:02", "1"])

        elif switch_name == 's2':
            controller.table_set_default("ipv4_lpm", "drop")
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.2.10/32"], ["00:00:0a:00:02:01", "2"])
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.0.0/16"], ["00:00:00:00:05:03", "1"])

        elif switch_name == 's3':
            controller.table_set_default("ipv4_lpm", "drop")
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.3.10/32"], ["00:00:0a:00:03:01", "2"])
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.3.20/32"], ["00:00:0a:00:03:02", "3"])
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.0.0/16"], ["00:00:00:00:06:02", "1"])

        elif switch_name == 's4':
            controller.table_set_default("ipv4_lpm", "drop")
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.4.10/32"], ["00:00:0a:00:04:01", "2"])
            controller.table_add("ipv4_lpm", "ipv4_forward", ["10.0.0.0/16"], ["00:00:00:00:06:03", "1"])

if __name__ == "__main__":
    Controller()