from .structs import *
from typing import Callable
import socket
class cirg:
    def __init__(self, host: str, port: int):
        self.dalib = dalim_t(
            host, 
            port, 
            lambda x: None, 
            socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        )
        self.clientOptions: ClientOptions = ClientOptions()
        self.sey: str = generate_random_string(20)
    
    def connect(self, how: int, timeout: int = 3) -> bool:
        for i in range(how):
            try:
                self.dalib.socket.settimeout(timeout)
                self.dalib.socket.connect((self.dalib.host, self.dalib.port))
                if(self.clientOptions.WantConnection == 0x02): self.dalib.socket.settimeout(None)
                data_to_send = self.clientOptions.fullBytes + self.sey.encode('utf-8')
                self.dalib.socket.send(data_to_send)
                
                return True
                
            except Exception as e:
                print(f"Connection attempt {i+1}/{how} failed: {e}")
                continue
        return False
    
    def getData(self, query: Callable[[bytes], None]) -> None:
        self.dalib.CallbackGetData = query
    
    def send_data(self, data: bytes) -> bool:        
        try:
            self.dalib.socket.send(packetManager.create_data_packet(data))
            return True
        except Exception as e:
            print(f"Send failed: {e}")
            return False
    
   
    
    def receive_loop(self, query: Callable[[bytes], None] = None) -> None:
        if query:
            self.dalib.CallbackGetData = query
        try:
            while(True):
                head = self.dalib.socket.recv(6)
                if len(head) < 6:
                    print("Incomplete header received")
                    self.close()
                    return
                parsHead = packetManager.parse_packet_header(head)
                if (parsHead['packet_type'] == 0x03):
                    data = self.dalib.socket.recv(parsHead['data_size'])
                    self.dalib.CallbackGetData(data)
                    
                    self.dalib.socket.send(packetManager.create_managment_packet(parsHead['hxcode']))


        except Exception as e:
            print(f"Receive error: {e}")
        finally:
            self.close()
    
    def close(self):
        if self.dalib.socket:
            self.dalib.socket.close()
            print("🔌 Connection closed")
