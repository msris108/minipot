import random
import sys

from minipot import shell_simulator
import logging
import threading
from socket import socket, timeout, gaierror
from time import sleep

BIND_IP_DEFAULT = '0.0.0.0'


class HoneyPot(object):

    def __init__(self, ports, logfile_path, bind_ip, verbose=False, rev_shell_enable=False):
        self.ports = ports

        self.ports = ports
        self.logfile_path = logfile_path
        self.listener_threads = {}
        self.bind_ip = bind_ip
        self.rev_shell_enable = rev_shell_enable

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%s',
                            filename=logfile_path,
                            filemode='w')
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing Honeypot.')
        print("press ctrl+c to stop listening")
        self.logger.info('Ports: %s' % self.ports)
        self.logger.info('Logfile: %s' % self.logfile_path)
        self.logger.info('Initialized Honeypot.')
        print('ON\tFROM\t\tTYPE\tPAYLOAD/INFO')
        if verbose:
            # console handler:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            self.logger.addHandler(console_handler)
        self.logger.debug('ON\t\tFROM\t\t\tTYPE\tPAYLOAD/INFO')

    def handle_connection(self, client_socket, port, ip, remote_port):
        flag = False
        self.logger.info("%s\t%s:%d\tCON.\tNil" % (port, ip, remote_port))  # CONNECTION
        client_socket.settimeout(5)
        try:
            data = client_socket.recv(64)
            self.logger.info("%s\t%s:%d\tDATA\t%s" % (port, ip, remote_port, data))  # PAYLOAD/info

            # SHELL SIMULATOR
            if self.rev_shell_enable:
                s = shell_simulator.run(data.decode('utf-8'))
                client_socket.send(s.encode('utf8'))
                sleep(1)

            client_socket.send(shell_simulator.get_random_string(random.randint(5, 20)).encode('utf8'))
            error_msg_1 = "\n[-] ERROR: PACKET DROPPED\n[-] CONN. LOST\n Reconnecting ...\n"
            client_socket.send(error_msg_1.encode('utf8'))
            sleep(3)
            client_socket.send("[-] Server timeout\n".encode('utf-8'))

        except timeout:
            client_socket.send("[-] Server timeout\n".encode('utf-8'))
            flag = True
            pass
        client_socket.close()
        if flag:
            self.logger.info("%s\t%s:%d\tDISCON.\tTimeout" % (port, ip, remote_port))  # DISCONNECTION
        else:
            self.logger.info("%s\t%s:%d\tDISCON.\tNil" % (port, ip, remote_port))  # DISCONNECTION

    def start_new_listener_thread(self, port):
        listener = socket()
        try:
            listener.bind((self.bind_ip, int(port)))
        except ValueError as v:
            print("--------------------------------------------------")
            print(v)
            print("Invalid / no valid port(s) found")
            print("recheck the config file and refer to the example")
            print("--------------------------------------------------")
            sys.exit(0)
        except gaierror as e:
            print("--------------------------------------------------")
            print(e)
            print(" [*] Using default host: 0.0.0.0 " )
            print("--------------------------------------------------")

            print('ON\tFROM\t\tTYPE\tPAYLOAD/INFO')
            self.bind_ip = BIND_IP_DEFAULT
            listener.bind((self.bind_ip, int(port)))
        listener.listen(5)

        while True:
            client, address = listener.accept()
            client_handler = threading.Thread(
                target=self.handle_connection,
                args=(client, port, address[0], address[1])
            )
            client_handler.start()

    def start_listening(self):
        for port in self.ports:
            self.listener_threads[port] = threading.Thread(target=self.start_new_listener_thread, args=(port,))
            self.listener_threads[port].start()

    def run(self):
        self.start_listening()
