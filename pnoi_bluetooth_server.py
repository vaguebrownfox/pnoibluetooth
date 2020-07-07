import bluetooth
import os 

class PnoiBlue :

    def __init__(self) :
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        self.port = self.server_sock.getsockname()[1]
        self.uuid = "93fd0c34-5cf0-4c07-8b12-06fcc82e17f0"


    def advertise(self) :
        bluetooth.advertise_service(self.server_sock, "Lno", service_id=self.uuid)

        print("Waiting for connection on RFCOMM channel...", self.port)

    def accept(self) :
        print("Waiting to accept...")
        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from", self.client_info)

    def read(self) :
        try:
            while True:
                self.data = self.client_sock.recv(1024)

                if not self.data:
                    print("not data")
                    break
                print(self.data)

                if self.data == b'record' :
                    os.system("echo Record start")
                elif self.data == b'stop' :
                    os.system("echo Record stop")
                elif self.data == b'download' :
                    os.system("echo Download start")
                    if (self.write()) :
                        break
                    
                print("reading")

                
        except OSError:
            print("OSError!!")
            pass

    def write(self) :
        with open('./rec.WAV', mode='rb') as f :
            data_bytes = f.read(10240)
            try :
                while data_bytes != b"" :
                    self.client_sock.send(data_bytes)
                    data_bytes = f.read(10240)
                    print(data_bytes)
                os.system("echo Download finished")
                return False
                #self.client_sock.close()
            except OSError :
                print("Write Error")
                return True
                pass
    
    def pnoiStart(self) :
        self.advertise()
        while True :
            self.accept()
            self.read()

    def pnoiDone(self) :
        self.client_sock.close()
        self.server_sock.close()
        print("All done.")




pnoiBlue = PnoiBlue()

pnoiBlue.pnoiStart()