from execredis.connection import ClientsConnection, ClusterClientsConnection


class ExecRedisClients:
    def __new__(cls, config, cluster=False):
        return ClusterClientsConnection(**config) if cluster else ClientsConnection(**config)
