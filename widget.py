from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit
from camadaFisica import CamadaFisica, GraphMaker
from camadaEnlace import CamadaEnlace, bitsToMessage
from receptor import Receptor
from transmissor import Transmissor
import matplotlib.pyplot as plt

def insertError(msg, probabilidadeErro):
    """
    Insere erros na mensagem com base na probabilidade fornecida.
    @param msg: Mensagem original
    @param probabilidadeErro: Probabilidade de erro (0 a 1)
    @return: Mensagem com erros inseridos
    """
    import random
    erro_msg = ""
    for bit in msg:
        if random.random() < probabilidadeErro:
            if bit == '1':
                erro_msg += '0'
            else:
                erro_msg += '1'
        else:
            erro_msg += bit

    return erro_msg

class MessageLayout(QWidget):

    def __init__(self):
        super().__init__()
        self.Layout = QHBoxLayout()
        self.Label = QLabel("Mensagem:")
        self.Input = QTextEdit()

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.Input)

        self.setLayout(self.Layout)

class MensagemAposErrorDetection(QWidget):
    def __init__(self):
        super().__init__()
        self.Layout = QHBoxLayout()
        self.Label = QLabel("Mensagem\n após deteção\n de erro")
        self.Text = QTextEdit()

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.Text)

        self.setLayout(self.Layout)

class MensagemAposEnquadramento(QWidget):
    def __init__(self):
        super().__init__()
        self.Layout = QHBoxLayout()
        self.Label = QLabel("Mensagem\n após\n enquadramento:")
        self.Text = QTextEdit()

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.Text)

        self.setLayout(self.Layout)

class MensagemAposHamming(QWidget):
    def __init__(self):
        super().__init__()
        self.Layout = QHBoxLayout()
        self.Label = QLabel("Mensagem\n após Hamming:")
        self.Text = QTextEdit()

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.Text)

        self.setLayout(self.Layout)

class MensagemEmBytes(QWidget):
    def __init__(self):
        super().__init__()
        self.Layout = QHBoxLayout()
        self.Label = QLabel("Mensagem em bits:")
        self.Text = QTextEdit()

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.Text)

        self.setLayout(self.Layout)


class EncodingOptions(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QHBoxLayout()
        self.Label = QLabel("Codificação:")
        self.NRZP_button = QPushButton("NRZP")
        self.Bipolar_button = QPushButton("Bipolar")
        self.Manchester_button = QPushButton("Manchester")

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.NRZP_button)
        self.Layout.addWidget(self.Bipolar_button)
        self.Layout.addWidget(self.Manchester_button)

        self.setLayout(self.Layout)

class ModulationOptions(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QHBoxLayout()
        self.Label = QLabel("Modulação:")
        self.FSK_button = QPushButton("FSK")
        self.ASK_button = QPushButton("ASK")
        self.PSK_button = QPushButton("PSK")

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.FSK_button)
        self.Layout.addWidget(self.PSK_button)
        self.Layout.addWidget(self.ASK_button)

        self.setLayout(self.Layout)

class OpcoesEnquadramento(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QHBoxLayout()
        self.Label = QLabel("Enquadramento:")
        self.Contagem_button = QPushButton("Contagem de caracteres")
        self.Bytes_button = QPushButton("Inserção de bytes")
        self.Bits_button = QPushButton("Inserção de bits")

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.Contagem_button)
        self.Layout.addWidget(self.Bytes_button)
        self.Layout.addWidget(self.Bits_button)

        self.setLayout(self.Layout)

class ErrorDetectionLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QHBoxLayout()
        self.Label = QLabel("Detecção de erro:")
        self.Paridade_button = QPushButton("Bit de paridade")
        self.CRC_button = QPushButton("CRC")

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.Paridade_button)
        self.Layout.addWidget(self.CRC_button)

        self.setLayout(self.Layout)

class SendButtonLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QHBoxLayout()
        self.Label = QLabel("Tamanho maximo de quadro:")
        self.LabelErro = QLabel("Probabilidade de erro:")
        self.InputTamanhoQuadro = QLineEdit()
        self.InputProbErro = QLineEdit()
        self.BotaoEnviar = QPushButton("Enviar")
        self.BotaoReceber = QPushButton("Receber")

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.InputTamanhoQuadro)
        self.Layout.addWidget(self.LabelErro)
        self.Layout.addWidget(self.InputProbErro)
        self.Layout.addWidget(self.BotaoEnviar)
        self.Layout.addWidget(self.BotaoReceber)

        self.setLayout(self.Layout)

class GraphButtonsLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QHBoxLayout()
        self.BotaoModulacao = QPushButton("Sinal modulado")
        self.BotaoCodificacao = QPushButton("Sinal codificado")

        self.Layout.addWidget(self.BotaoModulacao)
        self.Layout.addWidget(self.BotaoCodificacao)

        self.setLayout(self.Layout)

class MainWidget(QWidget):

    def __init__(self, server_addr = 'localhost', server_port = 64000, client_addr = 'localhost', client_port = 64001):
        super().__init__()
        self.setWindowTitle("interface de transmissão")
        self.mensagem_enviada_ou_recebida = ""

        # opções iniciais de enquadramento e detecção de erro
        self.Enquadramento = "Contagem"
        self.ErrorDetection = "ParityBit"
        self.listaQuadros = list()

        # declaracao das camadas
        self.CamadaFisica = CamadaFisica()
        self.CamadaEnlace = CamadaEnlace()

        # declaraco da classe que faz graficos
        self.GraphMaker = GraphMaker()

        # declaracao das classes de conexao
        self.receptor = Receptor(server_addr,server_port,on_data_received=self.mensagem_recebida)
        self.receptor.start()
        self.transmissor = Transmissor(client_addr, client_port)

        # declaracao de todos os componentes da interface
        self.MessageLayout = MessageLayout()
        self.EncodingOptionsLayout = EncodingOptions()
        self.ModulationOptionsLayout = ModulationOptions()
        self.LayoutEnquadramento = OpcoesEnquadramento()
        self.ErrorDetectionLayout = ErrorDetectionLayout()
        self.Mensagem_em_bytes = MensagemEmBytes()
        self.Mensagem_enquadramento = MensagemAposEnquadramento()
        self.Mensagem_error_detection = MensagemAposErrorDetection()
        self.Mensagem_hamming = MensagemAposHamming()
        self.Botao_enviar = SendButtonLayout()
        self.Botoes_grafico = GraphButtonsLayout()

        # conexao do layout de codificação com suas funções
        self.EncodingOptionsLayout.NRZP_button.clicked.connect(self.NRZP_clicked)
        self.EncodingOptionsLayout.Bipolar_button.clicked.connect(self.Bipolar_clicked)
        self.EncodingOptionsLayout.Manchester_button.clicked.connect(self.Manchester_clicked)

        # conexao do layout de modulação com suas funções
        self.ModulationOptionsLayout.ASK_button.clicked.connect(self.ASK_clicked)
        self.ModulationOptionsLayout.FSK_button.clicked.connect(self.FSK_clicked)
        self.ModulationOptionsLayout.PSK_button.clicked.connect(self.PSK_clicked)

        # conexao do layout de enquadramento com suas funções
        self.LayoutEnquadramento.Contagem_button.clicked.connect(self.Contagem_clicked)
        self.LayoutEnquadramento.Bytes_button.clicked.connect(self.ByteInsertion_clicked)
        self.LayoutEnquadramento.Bits_button.clicked.connect(self.BitInsertion_clicked)

        # conexao do layout de detecção de erro com suas funções
        self.ErrorDetectionLayout.Paridade_button.clicked.connect(self.ParityBit_clicked)
        self.ErrorDetectionLayout.CRC_button.clicked.connect(self.CRC_clicked)

        # conexao do layout de envio com suas funções
        self.Botao_enviar.BotaoEnviar.clicked.connect(self.Enviar_clicked)
        self.Botao_enviar.BotaoReceber.clicked.connect(self.Receber_clicked)

        # conexao da classe de graficos com suas funções
        self.Botoes_grafico.BotaoModulacao.clicked.connect(self.Modulado_clicked)
        self.Botoes_grafico.BotaoCodificacao.clicked.connect(self.Codificado_clicked)


        v_layout = QVBoxLayout()
        v_layout.addWidget(self.EncodingOptionsLayout)
        v_layout.addWidget(self.ModulationOptionsLayout)
        v_layout.addWidget(self.LayoutEnquadramento)
        v_layout.addWidget(self.ErrorDetectionLayout)
        v_layout.addWidget(self.MessageLayout)
        v_layout.addWidget(self.Botao_enviar)
        v_layout.addWidget(self.Mensagem_em_bytes)
        v_layout.addWidget(self.Mensagem_enquadramento)
        v_layout.addWidget(self.Mensagem_error_detection)
        v_layout.addWidget(self.Mensagem_hamming)
        v_layout.addWidget(self.Botoes_grafico)

        self.setLayout(v_layout)

    def NRZP_clicked(self):
        self.CamadaFisica.setModulacaoDigital("NRZP")
        print("codificacao trocada para: NRZP")

    def Bipolar_clicked(self):
        self.CamadaFisica.setModulacaoDigital("Bipolar")
        print("codificacao trocada para: bipolar")
        
    def Manchester_clicked(self):
        self.CamadaFisica.setModulacaoDigital("Manchester")
        print("codificacao trocada para: manchester")

    def ASK_clicked(self):
        self.CamadaFisica.setModulacaoAnalogica("ASK")
        print("modulacao trocada para: ASK")

    def FSK_clicked(self):
        self.CamadaFisica.setModulacaoAnalogica("FSK")
        print("modulacao trocada para: FSK")

    def PSK_clicked(self):
        self.CamadaFisica.setModulacaoAnalogica("PSK")
        print("modulacao trocada para: PSK")

    def Contagem_clicked(self):
        self.Enquadramento = "Contagem"
        print("metodo de contagem de caracteres selecionado")
    
    def ByteInsertion_clicked(self):
        self.Enquadramento = "ByteInsertion"
        print("metodo de inserçao de bytes selecionado")

    def BitInsertion_clicked(self):
        self.Enquadramento = "BitInsertion"
        print("metodo de inserçao de bits selecionado")

    def ParityBit_clicked(self):
        self.ErrorDetection = "ParityBit"
        print("correçao de erro com bit de paridade")

    def CRC_clicked(self):
        self.ErrorDetection = "CRC"
        print("correçao de erro com crc32")

    def Enviar_clicked(self):
        self.transmissor.connect(self.transmissor.host, self.transmissor.port)
        self.LimiteTamanhoQuadro = int(self.Botao_enviar.InputTamanhoQuadro.text())
        self.listaQuadros = []
        self.msg = self.MessageLayout.Input.toPlainText()
        self.Mensagem_em_bytes.Text.setText(self.CamadaEnlace.messageToBits(self.msg))
        self.listaQuadros = self.CamadaEnlace.sliceMessage(self.msg, self.LimiteTamanhoQuadro)
        self.listaQuadros = list(map(self.CamadaEnlace.messageToBits,self.listaQuadros))

        if(self.Enquadramento == "Contagem"):
            self.listaQuadros = list(map(self.CamadaEnlace.contagemCaracteres, self.listaQuadros))
        elif(self.Enquadramento == "ByteInsertion"):
            self.listaQuadros = list(map(self.CamadaEnlace.flag_byte_insertion, self.listaQuadros))
        elif(self.Enquadramento == "BitInsertion"):
            self.listaQuadros = list(map(self.CamadaEnlace.flagsBitInsertion, self.listaQuadros))

        self.msg_enquadrada = "".join(self.listaQuadros)

        self.Mensagem_enquadramento.Text.setText(self.msg_enquadrada)

        if(self.ErrorDetection == "ParityBit"):
            self.after_error_detection = self.CamadaEnlace.paridadePar(self.msg_enquadrada)
        elif(self.ErrorDetection == "CRC"):
            self.after_error_detection = self.CamadaEnlace.crc32Encode(self.msg_enquadrada)

        self.Mensagem_error_detection.Text.setText(self.after_error_detection)

        self.after_hamming = self.CamadaEnlace.hamming_encoder.hammingEncode(self.after_error_detection)

        self.Mensagem_hamming.Text.setText(self.after_hamming)

        self.mensagem_enviada_ou_recebida = self.after_hamming

        self.mensagem_codificada = self.CamadaFisica.encode(self.after_hamming)
        self.mensagem_modulada = self.CamadaFisica.modulate(self.after_hamming)

        # adicionar aqui logica para enviar mensagem para o socket, importante incluir mecanismo para mudar taxa de erro
        if (self.Botao_enviar.InputProbErro.text() != '' and self.Botao_enviar.InputProbErro.text() != '0'):
            probabilidadeErro = float(self.Botao_enviar.InputProbErro.text())
            msg_codificada_com_erro = insertError(self.after_hamming, probabilidadeErro)
            if self.after_hamming != msg_codificada_com_erro:
                print("Mensagem com erro inserido")
            self.mensagem_enviada_ou_recebida = self.transmissor.sendmsg(msg_codificada_com_erro.encode('utf-8'))
            print('Mensagem recebida:', self.mensagem_enviada_ou_recebida)
        else:
            self.mensagem_enviada_ou_recebida = self.transmissor.sendmsg(self.after_hamming.encode('utf-8'))
            print('Mensagem recebida:', self.mensagem_enviada_ou_recebida)

        self.transmissor.desconnect()

    def Receber_clicked(self):

        #self.mensagem_enviada_ou_recebida = atribuir aqui a mensagem vinda do socket

        try: # aqui tentamos detectar e corrigir erro de apenas 1 bit
            self.verificacaoHamming = self.CamadaEnlace.hamming_encoder.detectError(self.mensagem_enviada_ou_recebida)
            if(self.verificacaoHamming != 0):
                self.posicaoErro = self.verificacaoHamming - 1
                self.after_hamming = ""
                for i in range(0, len(self.mensagem_enviada_ou_recebida)):
                    if( i == self.posicaoErro ):
                        if(self.mensagem_enviada_ou_recebida == '0'):
                            self.after_hamming = self.after_hamming + '1'
                        else:
                            self.after_hamming = self.after_hamming + '0'
                    else:
                        self.after_hamming = self.after_hamming + self.mensagem_enviada_ou_recebida[i]
            self.after_hamming = self.CamadaEnlace.hamming_encoder.removeParityBits(self.after_hamming)
            self.Mensagem_hamming.Text.setText(self.after_hamming)

        except: # quando são detectados 2 bits errados, caímos nessa exceção, não é possível determinar a posição dos erros nem fazer sua correção
            self.after_hamming = self.CamadaEnlace.hamming_encoder.removeParityBits(self.mensagem_enviada_ou_recebida)
            self.Mensagem_hamming.Text.setText("Foram detectados 2 bits errados com a codificação Hamming, correção impossível")

        # aqui estao os protocolos de detecção de erro, caso algum erro seja detectado, será exibido um aviso de detecção ao invés da mensagem
        if(self.ErrorDetection == "ParityBit"):
            if(self.CamadaEnlace.verificaParidadePar(self.after_hamming) == "ok"):
                self.after_error_detection = self.CamadaEnlace.removeBitParidade(self.after_hamming)
                self.Mensagem_error_detection.Text.setText(self.after_error_detection)
            else:
                self.Mensagem_error_detection.Text.setText("Foi detectado erro com o bit de paridade")
                self.after_error_detection = self.CamadaEnlace.removeBitParidade(self.after_hamming)
        elif(self.ErrorDetection == "CRC"):
            if(self.CamadaEnlace.crc32Verify(self.after_hamming) == "ok"):
                self.after_error_detection = self.CamadaEnlace.crc32Remove(self.after_hamming)
                self.Mensagem_error_detection.Text.setText(self.after_error_detection)
            else:
                self.Mensagem_error_detection.Text.setText("Foi detectado erro com o CRC32")
                self.after_error_detection = self.CamadaEnlace.crc32Remove(self.after_hamming)

        self.ErroDeEnquadramento = False
        #aqui estao os protocolos pra desenquadrar a mensagem

        if(self.Enquadramento == "Contagem"):
            try:
                self.listaQuadros = self.CamadaEnlace.separaQuadrosContagemCaracteres(self.after_error_detection)
            except:
                self.ErroDeEnquadramento = True
                self.Mensagem_enquadramento.Text.setText("Foi detectado erro na contagem de caracteres")
        elif(self.Enquadramento == "ByteInsertion"):
            try:
                self.listaQuadros = self.CamadaEnlace.separaQuadrosByteInsertion(self.after_error_detection)
            except:
                self.ErroDeEnquadramento = True
                self.Mensagem_enquadramento.Text.setText("Foi detectado erro na inserção de bytes")
        elif(self.Enquadramento == "BitInsertion"):
            try:
                self.listaQuadros = self.CamadaEnlace.separaQuadrosBitInsertion(self.after_error_detection)
            except:
                self.ErroDeEnquadramento = True
                self.Mensagem_enquadramento.Text.setText("Foi detectado erro na inserção de bits")

        # caso haja erro de enquadramento, mostramos um erro e encerramos a tentativa de mostrar a mensagem
        if(self.ErroDeEnquadramento):
            self.MessageLayout.Input.setText("não foi possível recuperar a mensagem devido a erro de enquadramento")
            return
        else:
            self.msg_enquadrada = "".join(self.listaQuadros)
            self.Mensagem_enquadramento.Text.setText(self.msg_enquadrada)

        self.msg = bitsToMessage(self.msg_enquadrada)

        self.MessageLayout.Input.setText(self.msg)
        return

 
    def mensagem_recebida(self,mensagem):
        """
        Recebe a mensagem do receptor e atualiza os campos de texto correspondentes.
        @param mensagem: Mensagem recebida do receptor
        """
        self.mensagem_enviada_ou_recebida = mensagem


    def Modulado_clicked(self):
        
        self.GraphMaker.MakeModulatedGraph(self.mensagem_modulada)
        plt.imread("modulated.jpg")
        plt.show()


    def Codificado_clicked(self):

        if(self.CamadaFisica.modulacao_digital == "Manchester"):
            self.GraphMaker.MakeManchesterGraph(self.after_hamming, 10)
        else:
            self.GraphMaker.MakeEncodedGraph(self.after_hamming, 10)

        plt.imread("encoded.jpg")
        plt.show()