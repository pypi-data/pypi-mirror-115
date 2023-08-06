

if __name__ == "__main__":
    import traceback
    from airtest.core.api import *
    from poco.drivers.std.dumper import StdDumper
    from poco.drivers.std.attributor import StdAttributor
    from poco.freezeui.hierarchy import FrozenUIHierarchy


    auto_setup(__file__)

    from poco.drivers.unity3d import UnityPoco

    poco = UnityPoco()

    # poco.agent.hierarchy.dump()
    # hierarchy = FrozenUIHierarchy(StdDumper(poco.agent.c), StdAttributor(poco.agent.c))
    # print(hierarchy.dump())
    poco("1").click()
    # from poco.utils.simplerpc.rpcclient import RpcClient
    # from poco.freezeui.hierarchy import FrozenUIHierarchy
    # from poco.utils.simplerpc.transport.ws import WebSocketClient
    # from poco.utils.simplerpc.transport.tcp.main import TcpClient
    # from poco.drivers.unity3d.unity3d_poco import DEFAULT_ADDR
    # from poco.drivers.std.attributor import StdAttributor
    # from poco.drivers.std.dumper import StdDumper
    #
    # connect_device("Android:///")
    # addr = DEFAULT_ADDR
    # dev = device()
    # adb_port, _ = dev.adb.setup_forward('tcp:{}'.format(addr[1]))
    # adb_host = dev.adb.host or addr[0]
    # addr = adb_host, adb_port
    #
    # # initialize poco:
    # print("initializing Unity poco.", addr)
    # try:
    #     conn = TcpClient(addr)
    #     c = RpcClient(conn)
    #     c.DEBUG = False
    #     # self.c.run(backend=True)
    #     c.wait_connected()
    #     hierarchy = FrozenUIHierarchy(StdDumper(c), StdAttributor(c))
    # except Exception:
    #     traceback.print_exc()
    #     # 初始化失败:
    #     print("failed")
    #
    # print(111111111111, hierarchy.dump())