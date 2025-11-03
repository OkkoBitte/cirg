from .structs import *
from .server import cirg


#USE
"""
init
"""
#cirgClient = cirg.cirg("ip",port)

"""
funtion from get data
"""
#def data_handler(data: bytes): 
#   print(f"Received str {bytes.decode(data)}")

"""
activation
"""
#cirgClient.getData(data_handler)
#cirgClient.receive_loop()



__all__ = ['cirg', 'dalim_t', 'ClientOptions', 'mazor_code']
