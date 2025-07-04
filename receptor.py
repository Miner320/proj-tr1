import socket as skt
from threading import Thread

class Receptor:
    def __init__(self, host = 'localhost', port = 64000):
        """!
        Inicializa o receptor com o endereço do servidor.
        @param host: Endereço IP do servidor
        @param port: Porta do servidor
        """
        if not isinstance(port, int):
            port = int(port)

        self.host = host
        self.port = port
        self.running = True
        self.data = []
        self.server_thread: Thread

    def start(self):
        """!
        Inicia o servidor para receber mensagens.
        """
        self.server_thread = Thread(target=self._start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def send_response(self, conn, message):
        """!
        Envia uma resposta ao cliente.
        @param conn: Conexão com o cliente
        @param message: Mensagem a ser enviada
        """
        try:
            conn.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f'Erro ao enviar resposta: {e}')

    def _start_server(self):
        sock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print('Servidor iniciado com sucesso!')
        while self.running:
            conn, addr = sock.accept()
            print(f'Conectado por {addr}')
            try:
                data = conn.recv(1024)
                if not data:
                    break
                self.data.append(data.decode('utf-8'))
                print(f'Mensagem recebida: {self.data[-1]}')
                resp = data.decode('utf-8') + " Cliente: " + addr[0] + ":" + str(addr[1])
                conn.send(resp.encode('utf-8'))  # Envia de volta a última mensagem recebida
            except Exception as e:
                print(f'Erro ao receber dados: {e}')
            finally:
                conn.close()

    def stop(self):
        """!
        Para o servidor e encerra a thread.
        """
        self.running = False
        if self.server_thread.is_alive():
            self.server_thread.join()
        print('Servidor parado.')

if __name__ == '__main__':
    receptor = Receptor()
    receptor.start()

    try:
        while True:
            pass  # Mantém o receptor ativo
    except KeyboardInterrupt:
        receptor.stop()
        print('Receptor encerrado.')