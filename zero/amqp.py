from pkg_resources import resource_filename
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import ClientCreator
from twisted.python import log
import txamqp.spec
from txamqp.protocol import AMQClient
from txamqp.client import TwistedDelegate
from celery import conf

amqp_file = resource_filename(__name__, 'amqp0-8.xml')
spec = txamqp.spec.load(amqp_file)

@inlineCallbacks
def got_connection(connection, username, password):
    print 'Connected to broker'
    yield connection.authenticate(username, password)
    print 'Authenticated'
    chan = yield connection.channel(1)
    yield chan.channel_open()

    print 'Closing connection'
    chan0 = yield connection.channel(0)
    yield chan0.connection_close()

def connect_to_server():
    host = conf.BROKER_HOST
    port = conf.BROKER_PORT
    vhost = conf.BROKER_VHOST
    username = conf.BROKER_USER
    password = conf.BROKER_PASSWORD

    delegate = TwistedDelegate()
    d = ClientCreator(reactor, AMQClient, delegate=delegate, vhost=vhost,
                      spec=spec).connectTCP(host, int(port))
    d.addCallback(got_connection, username, password)

    def errback(err):
        if reactor.running:
            log.err(err)
            reactor.stop()
    d.addErrback(errback)
