import atexit
import time
import traceback
import zmq


class XPlaneClient:

    def __init__(self, topic, ip="127.0.0.1", sub_port=5555, pub_port=5556):

        zmq.RCVTIMEO = 1000

        # Initialize a zeromq context
        self.context = zmq.Context()
        self.ip = ip
        self.topic = topic

        publisher_port = pub_port
        subscriber_port = sub_port

        self.subscription_port = subscriber_port
        self.publication_port = publisher_port

        self.sleep_time = 1.5
        
        atexit.register(self.disconnect)

    def connect(self):
        """
        Connect to the C++ client. Make sure that Xplane and the C++ client are running

        """
        
        # Set up a channel to send work

        try:
            self.publisher = self.context.socket(zmq.PUB)
            self.publisher.bind(f"tcp://{self.ip}:{self.publication_port}") # Initialization port

            self.subscriber = self.context.socket(zmq.SUB)
            self.subscriber.RCVTIMEO = 5000
            self.subscriber.connect(f"tcp://{self.ip}:{self.subscription_port}")
            self.subscriber.subscribe(self.topic)

            # Give everything a second to spin up and connect
            time.sleep(self.sleep_time)

            # Send initial connection string to register to server
            self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"Connection"])
            time.sleep(self.sleep_time)

            response = self.subscriber.recv_multipart()
        except:
            # Wait till socket is available
            self.subscriber.close()
            self.publisher.close()
            print(f"{self.topic} did not connect successfully")
            return False
                
        # Give everything a second to spin up and connect
        time.sleep(self.sleep_time)

        # Disconnect and unbind from old sockets
        self.publisher.unbind(f"tcp://{self.ip}:{self.publication_port}")
        self.subscriber.disconnect(f"tcp://{self.ip}:{self.subscription_port}")
        
        self.publication_port = response[1].decode("utf-8")
        self.subscription_port = response[2].decode("utf-8")
        print(f"{self.topic} connected to Xplane Server on publication {self.publication_port} port and subscription {self.subscription_port} port")

        # Rebind the connection for the new ports
        self.publisher.bind(f"tcp://{self.ip}:{self.publication_port}")
        self.subscriber.connect(f"tcp://{self.ip}:{self.subscription_port}")

        # Give everything a second to spin up and connect
        time.sleep(self.sleep_time)
        return True

    def disconnect(self):
        # Send disconnection message to server
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"Disconnection", b"0", b"0"])
        response = self.subscriber.recv_multipart()

        # Give everything a second
        time.sleep(self.sleep_time)

        if "Received" in response[1].decode("utf-8"):
            self.subscriber.disconnect(f"tcp://{self.ip}:{self.subscription_port}")
            self.publisher.unbind(f"tcp://{self.ip}:{self.publication_port}")
            self.subscriber.close()
            self.publisher.close()
            self.context.term()
            print(f"{self.topic} disconnected")
            return True
        else:
            return False


    def getDataRef(self, dref):
        """
        Get the value of a dataref as a string.

        Args:
            response (set): dataRef of interest as a string, time elasped since last update of dataref in seconds

        Returns:
            str: Value of the dataRef
        """
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"read", bytes(dref, 'utf-8'), b"0"])
        response = self.subscriber.recv_multipart()
        return response[1].decode("utf-8"), response[2].decode("utf-8")

    def setDataRef(self, dref, value, verbose=False):
        """
        Set the dataref to the specified value.

        Args:
            dref (str): Dataref of interest
            value (str): Value of the dataref

        Returns:
            bool: True of successfully sent, false otherwise.
        """
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"set", bytes(dref, 'utf-8'), bytes(value, 'utf-8')])
        response = self.subscriber.recv_multipart()
        response_message = response[1].decode("utf-8")
        
        if verbose:
            print(response_message)
        
        if "Received" in response_message:
            return 0
        elif "Error" in response_message:
            return 1
        else:
            return 2
            
    def terminate(self, verbose=False):
        """
        Liberate position of writer

        Returns:
            bool: True of successfully sent, false otherwise.
        """
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"terminate", b"0", b"0"])
        response = self.subscriber.recv_multipart()
        response_message = response[1].decode("utf-8")
        
        if verbose:
            print(response_message)
        
        if "Received" in response_message:
            return 0
        elif "Error" in response_message:
            return 1
        else:
            return 2

    def sendCommand(self, dref, verbose=False):
        """
        Send command to Xplane.

        Args:
            dref (str): Designated command to be sent

        Returns:
            bool: True of successfully sent, false otherwise.
        """
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"command", bytes(dref, 'utf-8'), b"0"])
        response = self.subscriber.recv_multipart()
        
        if "Received" in response[1].decode("utf-8"):
            return 0
        else:
            return 1


