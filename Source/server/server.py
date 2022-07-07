import socket
import json 
import numpy as np 
import cv2
import time 

BUFFER_SIZE = 2 ** 15

def read_img_to_bytes(img_path, dsize = (-1, -1)): 
  """
  Read image, then resize and convert to bytes 
  :param img_path: URL of image 
  :param dsize: Size of image that want to resize, if (-1, -1) 
                then size of image is original
  :return: bytes of image after resize
  """
  img = cv2.imread(img_path) 
  if (dsize[0] != -1): 
    img = cv2.resize(img, dsize = dsize) 
  return cv2.imencode('.jpg', img)[1]
  
""" Database """
class Database: 
  """ 
  Attribute: 
    db: Content of json file 
  """

  def __init__(self, DB_PATH): 
    """
    Initialize database 
    :param DB_PATH: URL of json file
    """
    f = open(DB_PATH) 
    self.db = json.load(f) 
    f.close() 

  def find_index(self, id_place): 
    """
    Find index of place in database with id 
    :param id_place: Id of place 
    :return: index of place in database
    """
    for index, item in enumerate(self.db): 
      if (item['id'] == id_place): 
        return index 
    return -1

  def get_information(self, index):  
    """
    Get information of index place in database 
    :param index: Index of place in database 
    :return: Information of place including id, name, latitude, longitude, description
    """
    return  {'id': self.db[index]['id'], 
            'name': self.db[index]['name'], 
            'latitude': self.db[index]['latitude'], 
            'longitude': self.db[index]['longitude'], 
            'description': self.db[index]['description']}
    
  def get_length(self): 
    """
    Get number of places 
    :return: Number of places
    """
    return len(self.db)

  def get_avatar(self, id): 
    """
    Get URL of avatar's place having id
    :param id: id place
    :return: URL of avatar
    """
    index = self.find_index(id)
    return self.db[index]['avatar']

  def get_detail_image(self, id):
    """
    Get list URL of images' place having id
    :param id: id place
    :return: List URL
    """
    index = self.find_index(id)
    return self.db[index]['detail_image']
  
""" UDP server socket """
class UDPServer: 
  """ 
  Attribute: 
    sk: UDP server socket 
    db: Database
  """

  def __init__(self, HOST, PORT, DB_PATH): 
    """
    Initialize UDP server
    :param HOST: Address of UDP server socket 
    :param PORT: Port of UDP server socket 
    :param DB_PATH: URL of file json (database)
    """
    print('Starting UDP server')
    self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    self.sk.bind((HOST, PORT)) 
    self.db = Database(DB_PATH)

  def __del__(self): 
    print('Closing UDP server')
    self.sk.close()

  def recv_request(self):
    """
    Receive request from client 
    :return: request after decode to string, address of client 
    """ 
    buffer = self.sk.recvfrom(BUFFER_SIZE) 
    return buffer[0].decode(), buffer[1]

  def send_msg(self, clientAddr, msg): 
    """
    Send message to UDP client socket 
    :param clientAddr: Address of UDP client 
    :param msg: Message sent to client 

    Divide message into <num_dgram> block of bytes, each block 
    has maximum <BUFFER_SIZE> bytes. Send each block in turn to 
    UDP client.
    """ 
    if (len(msg) == 0): 
      return

    # Find number of blocks 
    num_dgram = (len(msg) - 1) // BUFFER_SIZE + 1
    self.sk.sendto(str(num_dgram).encode(), clientAddr) 

    # Send message to UDP client 
    for i in range(num_dgram): 
      current_msg = msg[i * BUFFER_SIZE : (i + 1) * BUFFER_SIZE]
      self.sk.sendto(current_msg, clientAddr)
      time.sleep(1e-20)

  def send_number_place(self, clientAddr): 
    """
    Send number of places to UDP client 
    :param clientAddr: Address of UDP client 
    """ 
    self.send_msg(clientAddr, str(self.db.get_length()).encode())

  def send_information_index(self, clientAddr, index): 
    """
    Send information of place to UDP client 
    :param clientAddr: Address of UDP client 
    :param index: Index of place in database
    """ 
    infor = self.db.get_information(index)
    self.send_msg(clientAddr, infor['id'].encode())
    self.send_msg(clientAddr, infor['name'].encode())
    self.send_msg(clientAddr, infor['latitude'].encode())
    self.send_msg(clientAddr, infor['longitude'].encode())
    self.send_msg(clientAddr, infor['description'].encode())

  def send_all_information(self, clientAddr): 
    """
    Send information of all place to UDP client 
    :param clientAddr: Address of UDP client 
    """ 
    self.send_number_place(clientAddr)
    for index in range(self.db.get_length()): 
      self.send_information_index(clientAddr, index)
  
  def send_information_id(self, clientAddr, id): 
    """
    Send information of place having id to UDP client 
    :param clientAddr: Address of UDP client 
    :param id: ID of place 
    """ 
    index = self.db.find_index(id)
    self.send_information_index(clientAddr, index) 

  def send_avatar_id(self, clientAddr, id, dsize = (-1, -1)): 
    """
    Send avatar of place having id to UDP client 
    :param clientAddr: Address of UDP client 
    :param id: ID of place 
    :dsize: size of avatar
    """ 
    avatar = read_img_to_bytes(self.db.get_avatar(id), dsize) 
    self.send_msg(clientAddr, avatar)

  def send_one_detail_image_id(self, clientAddr, id, index_img, dsize = (-1, -1)): 
    """
    Send one detail image of place to UDP client 
    :param clientAddr: Address of UDP client 
    :param id: ID of place 
    :param index_img: index of image 
    :dsize: size of image
    """ 
    all_img_path = self.db.get_detail_image(id)
    img = read_img_to_bytes(all_img_path[index_img], dsize) 
    self.send_msg(clientAddr, img)

  def send_detail_image_id(self, clientAddr, id, dsize = (-1, -1)): 
    """
    Send all detail images of place to UDP client 
    :param clientAddr: Address of UDP client 
    :param id: ID of place  
    :dsize: size of image
    """ 
    all_img_path = self.db.get_detail_image(id)
    self.send_msg(clientAddr, str(len(all_img_path)).encode())
    for img_path in all_img_path: 
      img = read_img_to_bytes(img_path, dsize) 
      self.send_msg(clientAddr, img)
  
  def handle_request(self, request, clientAddr): 
    """
    Handle request, reply to UDP client 
    :param request: request from UDP client 
    :param clientAddr: Address of UDP client 

    Request: 
      get all information: reply information of all places
      get information id <id>: reply information of place having id
      get avatar <id> <dim1> <dim2>: reply avatar with size (dim1, dim2) 
          as bytes of place having id
      get detail image <id> <dim1> <dim2>: reply all detail image with 
          size (dim1, dim2) as bytes of place having id
      get one image <id> <index_img> <dim1> <dim2>: reply <index_img>th 
          image with size (dim1, dim2) as bytes of place having id
    """ 
    if (request.startswith('get all information')): 
      self.send_all_information(clientAddr)
    elif (request.startswith('get information id')): 
      self.send_information_id(clientAddr, request.split()[-1])
    elif (request.startswith('get avatar')): 
      in4 = request.split()[-3:] 
      self.send_avatar_id(clientAddr, in4[0], dsize = (int(in4[1]), int(in4[2])))
    elif (request.startswith('get detail image')):
      in4 = request.split()[-3:] 
      self.send_detail_image_id(clientAddr, in4[0], dsize = (int(in4[1]), int(in4[2])))
    elif (request.startswith('get one detail image')): 
      in4 = request.split()[-4:] 
      self.send_one_detail_image_id(clientAddr, in4[0], int(in4[1]), dsize = (int(in4[2]), int(in4[3])))

  def start(self): 
    while (True): 
      print('UDP Server is listening...')
      request, clientAddr = self.recv_request()
      print('Message: {}\nFrom Client: {}'.format(request, clientAddr))
      self.handle_request(request, clientAddr)


HOST = '127.0.0.1' 
PORT = 43210
DB_PATH = './database/place.json'

server = UDPServer(HOST, PORT, DB_PATH)
server.start()

