"""
Where solution code to project should be written.  No other files should
be modified.
"""

import socket
import io
import time
import typing
import struct
import util
import util.logging
import pickle

class send_packet:
    def __init__(self, seq, data):
        self.seq = seq
        self.data = data
        #print(self.seq)
        #print(self.data)
    def encode(self):
        send_data = bytearray(self.data)
        list = [self.seq, send_data]
        #print(list)
        return list


class recv_packet:
    def __init__(self, ack):
        pack.ack = ack




def send(sock: socket.socket, data: bytes):
    """
    Implementation of the sending logic for sending data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.
        data -- A bytes object, containing the data to send over the network.
    """

    # Naive implementation where we chunk the data to be sent into
    # packets as large as the network will allow, and then send them
    # over the network, pausing half a second between sends to let the
    # network "rest" :)
    logger = util.logging.get_logger("project-sender")
    chunk_size = util.MAX_PACKET - 100
    pause = .1
    offsets = range(0, len(data), util.MAX_PACKET - 100)
    index = 0
    for chunk in [data[i:i + chunk_size] for i in offsets]:
        send_pack = send_packet(index, chunk)
        msg = pickle.dumps(send_pack)
        sock.send(msg)#bytearray([index, chunk]))#msg)
        index+=1
        logger.info("Pausing for %f seconds", round(pause, 2))
        time.sleep(pause)


def recv(sock: socket.socket, dest: io.BufferedIOBase) -> int:
    """
    Implementation of the receiving logic for receiving data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.

    Return:
        The number of bytes written to the destination.
    """
    logger = util.logging.get_logger("project-receiver")
    # Naive solution, where we continually read data off the socket
    # until we don't receive any more data, and then return.
    num_bytes = 0
    while True:
        data = sock.recv(util.MAX_PACKET)
        if not data:
            break
        received_pack = pickle.loads(data)
        #decoded_data = data.decode()
        #send_pack = send_packet(decoded_data[0],decoded_data[1])
        logger.info("Received %d bytes", len(data))
        dest.write(received_pack.data)#data)#send_pack.data)#received_pack.data)#
        num_bytes += len(received_pack.data)#received_pack.data)#data)
        dest.flush()
    return num_bytes
