from logging.handlers import DatagramHandler

from logstash_sync.handler_tcp import TCPLogstashHandler


class UDPLogstashHandler(TCPLogstashHandler, DatagramHandler):
    """Python logging handler for Logstash. Sends events over UDP.
    :param host: The host of the logstash_sync server.
    :param port: The port of the logstash_sync server (default 5959).
    :param message_type: The type of the message (default logstash_sync).
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstash_sync event schema (default is 0).
    :param tags: list of tags for a logger (default is None).
    """

    def makePickle(self, record):
        return self.formatter.format(record)
