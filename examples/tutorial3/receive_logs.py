#! /usr/bin/env python
from tornado.ioloop import IOLoop
from stormed import Connection, Message

ch = None

def on_connect():
    global ch
    ch = conn.channel()
    ch.exchange_declare(exchange='logs', type='fanout')
    ch.queue_declare(exclusive=True, callback=with_temp_queue)

def with_temp_queue(queue_name, message_count, consumer_count):
    ch.queue_bind(exchange='logs', queue=queue_name)
    ch.consume(queue_name, callback, no_ack=True)

def callback(msg):
    print " [x] %r" % msg.body

conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
print ' [*] Waiting for logs. To exit press CTRL+C'
try:
    io_loop.start()
except KeyboardInterrupt:
    conn.close(io_loop.stop)
