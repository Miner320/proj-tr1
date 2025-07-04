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

    def sendmsg(self,msg,is_signal=False):
        """!
        Envia uma mensagem para o servidor.
        @param msg: Mensagem a ser enviada
        """
        if is_signal:
            msg_traduzida = ''
            for term in msg:
                print(term)
                msg_traduzida += str(term) + ' '
            self.sock.sendall(msg_traduzida.encode('utf-8'))
        else:
            self.sock.sendall(msg)

        recvmsg = self.sock.recv(1024)

        if recvmsg != b'':
            recvmsg = "Sucesso!".encode('utf-8')

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