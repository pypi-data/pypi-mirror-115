from execredis.connection import ClientsConnection, ClusterClientsConnection


class ExecRedisClients:
    def __new__(cls, config, cluster=False):
        return ClusterClientsConnection(**config) if cluster else ClientsConnection(**config)

    @classmethod
    def create(cls, client: str, clients_config: dict):
        _config = dict(clients_config[client])
        return cls(_config, cluster=_config.pop("cluster", False))
