import socket as skt

class Transmissor:
    def __init__(self, server_address='localhost', server_port=64000):
        """!
        Inicializa o transmissor com o endereço do servidor.
        @param server_addres: Endereço IP do servidor
        @param server_port: Porta do servidor
        """
        self.host = server_address
        self.port = server_port
        self.sock = None

    def connect(self, server_address, server_port):
        """!
        Conecta ao servidor.
        @return: Objeto socket conectado ao servidor
        """
        if not isinstance(server_port, int):
            server_port = int(server_port)

        self.sock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.sock.connect((server_address, server_port))

    def sendmsg(self,msg):
        """!
        Envia uma mensagem para o servidor.
        @param msg: Mensagem a ser enviada
        """
        self.sock.sendall(msg)

        recvmsg = self.sock.recv(1024)

        return recvmsg.decode('utf-8')

    def desconnect(self):
        """!
        Desconecta do servidor.
        """
        if self.sock:
            self.sock.shutdown(skt.SHUT_RDWR)
            self.sock.close()
            self.sock = None
        else:
            print("Nenhuma conexão ativa para desconectar.")

if __name__ == '__main__':
    transmissor = Transmissor()
    transmissor.connect('localhost', 64000)
    mensagem = "Olá, servidor!"
    print(f"Enviando mensagem: {mensagem}")
    resposta = transmissor.sendmsg(mensagem.encode('utf-8'))
    print(f"Resposta do servidor: {resposta}")