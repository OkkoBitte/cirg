import cirg


cirgClient = cirg.cirg("web-mbg.ru",333)


if (cirgClient.connect(3)): print("Connected!")



def data_handler(data: bytes): print(f"Received data: {data}")

cirgClient.send_data(cirgClient.sey.encode('utf-8')+b'\x01'+b"hello")
cirgClient.getData(data_handler)
cirgClient.receive_loop()