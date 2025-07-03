import socket as skt

class Transmissor:
    def __init__(self):
        """!
        Inicializa o transmissor com o endereço do servidor.
        @param host: Endereço IP do servidor
        @param port: Porta do servidor
        """
        self.sock = None

    def connect(self, server_address, server_port):
        """!
        Conecta ao servidor.
        @return: Objeto socket conectado ao servidor
        """
        self.sock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.sock.connect((server_address, server_port))

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
    transmissor = Transmissor()
    transmissor.connect('localhost', 64000)
    mensagem = "Olá, servidor!"
    print(f"Enviando mensagem: {mensagem}")
    resposta = transmissor.sendmsg(mensagem)
    print(f"Resposta do servidor: {resposta}")