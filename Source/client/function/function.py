import socket
import numpy as np 
import cv2
from PIL import Image
import io

BUFFER_SIZE = 2 ** 15

def cvt_bytes2pilimage(img_bytes): 
    """
    Convert bytes to PIL image 
    :param img_bytes: bytes 
    :return: PIL image converted from bytes
    """
    img = Image.open(io.BytesIO(img_bytes))
    return img

def makeClient(SERVER_ADDR):
    return UDPClient(SERVER_ADDR)

""" UDP client socket """
class UDPClient: 
    """ 
    Attribute: 
        serverAddr: Address of UDP server 
        sk: socket 
    """

    def __init__(self, serverAddr): 
        """
        Initialize UDP client
        :param serverAddr: Address of UDP server 
        """
        print('Starting UDP client')
        self.serverAddr = serverAddr
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __del__(self): 
        print('Closing UDP client')
        self.sk.close()

    def send_request(self, request):  
        """
        Send request to UDP server 
        :param: request sent to server 
        """
        self.sk.sendto(request, self.serverAddr)

    def recv_msg(self): 
        """
        Receive message from UDP server 
        :return: message as bytes 

        S1: receive number of datagrams <num_dgram> sent 
        from UDP server.
        S2: receive <num_dgram> from UDP server.
        """
        buffer = self.sk.recvfrom(BUFFER_SIZE) 
        num_dgram = int(buffer[0].decode())
        res_bytes = b''
        for i in range(num_dgram): 
            buffer = self.sk.recvfrom(BUFFER_SIZE) 
            res_bytes += buffer[0] 
        return res_bytes

    def recv_int(self): 
        """
        Receive integer from UDP server 
        :return: integer
        """
        num = int(self.recv_msg().decode())
        return num

    def recv_information(self): 
        """
        Receive information of a place from UDP server 
        :return: information of a place 
        """
        place = {} 
        place['id'] = self.recv_msg().decode()
        place['name'] = self.recv_msg().decode()
        place['latitude'] = self.recv_msg().decode()
        place['longitude'] = self.recv_msg().decode()
        place['description'] = self.recv_msg().decode()
        return place

    def request_all_information(self): 
        """
        Request server for information of all places 
        :return: information of all places 
        """
        self.send_request('get all information'.encode())
        num_places = self.recv_int()
        list_places = []
        for i in range(num_places): 
            list_places.append(self.recv_information())
        return list_places

    def request_information_id(self, id): 
        """
        Request server for information of place with id 
        :param id: ID of place 
        :return: information of place with id
        """
        self.send_request(f'get information id {id}'.encode()) 
        return self.recv_information() 

    def request_avatar(self, id, dsize = (-1, -1)): 
        """
        Request server for avatar size = dsize of place with id 
        :param id: ID of place 
        :param dsize: size of avatar 
        :return: avatar of place as PIL image 
        """
        self.send_request(f'get avatar {id} {dsize[0]} {dsize[1]}'.encode())
        return cvt_bytes2pilimage(self.recv_msg())

    def request_detail_image(self, id, dsize = (-1, -1)):
        """
        Request server for all images size = dsize of place with id 
        :param id: ID of place 
        :param dsize: size of images
        :return: all images of place as PIL image 
        """
        self.send_request(f'get detail image {id} {dsize[0]} {dsize[1]}'.encode())
        num_image = self.recv_int() 
        list_img = [] 
        for i in range(num_image): 
            list_img.append(cvt_bytes2pilimage(self.recv_msg())) 
        return list_img
    
    def request_one_detail_image(self, id, index_img, dsize = (-1, -1)):
        """
        Request server for one image size = dsize of place with id 
        :param id: ID of place 
        :param index_img: index of image 
        :param dsize: size of images
        :return: one image of place as PIL image
        """
        self.send_request(f'get one detail image {id} {index_img} {dsize[0]} {dsize[1]}'.encode())
        return cvt_bytes2pilimage(self.recv_msg())
