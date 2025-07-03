import socket as skt
from camadaFisica import CamadaFisica



class Transmissor:
    def __init__(self, host, port):
        """!
        Inicializa o transmissor com o endereço do servidor.
        @param host: Endereço IP do servidor
        @param port: Porta do servidor
        """
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        """!
        Conecta ao servidor.
        @return: Objeto socket conectado ao servidor
        """
        self.sock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def sendmsg(self,msg):
        """!
        Envia uma mensagem para o servidor.
        @param msg: Mensagem a ser enviada
        """
        self.sock.sendall(msg.encode('utf-8'))

        recvmsg = self.sock.recv(1024)

        self.sock.close()

        return recvmsg.decode('utf-8')

if __name__ == '__main__':
    transmissor = Transmissor('localhost', 64000)
    transmissor.connect()
    mensagem = "Olá, servidor!"
    print(f"Enviando mensagem: {mensagem}")
    resposta = transmissor.sendmsg(mensagem)
    print(f"Resposta do servidor: {resposta}")