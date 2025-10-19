import random, string
from typing import Callable
import socket


def generate_random_string(length=20):
    characters = string.ascii_letters + string.digits  
    return ''.join(random.choices(characters, k=length))
class ClientOptions:
    def __init__(self, 
                 TypeClient: str = "new", 
                 WantConnection: str = "keep-alive", 
                 ActionFromPassivation: int = 255, 
                 TimeToSleep: int = 255, 
                 TypeConnection: str = "normal",
                 mazor_code: int = 0x01):
        

        self.TypeClient = 0x00
        self.WantConnection = 0x00
        self.ActionFromPassivation = 0x00
        self.TimeToSleep = 0x00
        self.TypeConnection = 0x00
        self.mazor_code = mazor_code

        if TypeClient == "new":
            self.TypeClient = 0x01
        
        if WantConnection == "keep-alive":
            self.WantConnection = 0x02
        elif WantConnection == "get-close":
            self.WantConnection = 0x01
        
        if 0 <= ActionFromPassivation <= 255:
            self.ActionFromPassivation = ActionFromPassivation
        
        if 0 <= TimeToSleep <= 255:
            self.TimeToSleep = TimeToSleep
        
        if TypeConnection == "normal":
            self.TypeConnection = 0x00
        
    def getFullBytes(self):
        return bytes([
            self.TypeClient,
            self.WantConnection, 
            self.ActionFromPassivation,
            self.TimeToSleep,
            self.TypeConnection,
            0x00, 0x00, 0x00, 0x00,  
            self.mazor_code & 0xFF
        ])

class dalim_t:
    def __init__(self, host: str, port: int, callback: Callable[[bytes], None], sock: socket.socket):
        self.host = host
        self.port = port
        self.CallbackGetData = callback
        self.socket = sock

class packetManager:
    def create_data_packet(data: bytes) -> bytes:
        packet_type = 0x03
        hxcode = [random.randint(0, 255), random.randint(0, 255)]

        timeout = 255
        
        data_size = len(data)
        datasize = [
            data_size & 0xFF,
            (data_size >> 8) & 0xFF
                    
        ]
        
        header = bytes([packet_type, hxcode[0], hxcode[1], timeout, datasize[0], datasize[1]])
        
        return header + data
    def create_managment_packet(hex:bytes) -> bytes:
        packet_type = 0x01
        hxcode = hex
        timeout = 255
        
          
        datasize = [
            0x00, 
            0x00          
        ]
        
        header = bytes([packet_type, hxcode[0], hxcode[1], timeout, datasize[0], datasize[1]])
        

        
        return header
    
    def parse_packet_header(header: bytes) -> dict:
        if len(header) != 6:
            raise ValueError("Header must be exactly 6 bytes long")
        
        packet_type = header[0]
        hxcode = [header[1], header[2]]
        timeout = header[3]
        data_size = header[5] | (header[4] << 8)  
        
        return {
            "packet_type": packet_type,
            "hxcode": hxcode,
            "timeout": timeout,
            "data_size": data_size
        }