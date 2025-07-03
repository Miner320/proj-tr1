import socket as skt

class Transmissor:
    def __init__(self):
        """!
        Inicializa o transmissor com o endereço do servidor.
        @param host: Endereço IP do servidor
        @param port: Porta do servidor
        """
        self.sock = None

    def error_insert(self,msg, qtd_erros):
        """!
        Insere um erro na mensagem.
        @param bytes: quantidade de bytes a serem alterados
        @return: Mensagem com erro inserido
        """
        # Insere um erro aleatório na mensagem
        import random
        if qtd_erros > 0:
            for i in range(qtd_erros):
                msg_com_erro = msg
                index = random.randint(0, len(msg) - 1)
                msg_com_erro = msg_com_erro[index] ^ 0xFF
        else:
            msg_com_erro = msg

        return msg_com_erro

    def connect(self, server_address, server_port):
        """!
        Conecta ao servidor.
        @return: Objeto socket conectado ao servidor
        """
        self.sock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.sock.connect((server_address, server_port))

    def sendmsg(self,msg, qtd_erros=0):
        """!
        Envia uma mensagem para o servidor.
        @param msg: Mensagem a ser enviada
        """
        if qtd_erros > 0:
            msg = self.error_insert(msg, qtd_erros)

        self.sock.sendall(msg)

        recvmsg = self.sock.recv(1024)

        self.sock.close()

        return recvmsg.decode('utf-8')

if __name__ == '__main__':
    transmissor = Transmissor()
    transmissor.connect('localhost', 64000)
    mensagem = "Olá, servidor!"
    print(f"Enviando mensagem: {mensagem}")
    resposta = transmissor.sendmsg(mensagem.encode('utf-8'))
    print(f"Resposta do servidor: {resposta}")