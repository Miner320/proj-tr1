from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit
from camadaFisica import CamadaFisica, GraphMaker
from camadaEnlace import CamadaEnlace
from receptor import Receptor
from transmissor import Transmissor
import matplotlib.pyplot as plt


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
        #self.receptor = Receptor(server_addr,server_port)
        self.transmissor = Transmissor()
        #self.transmissor.connect(client_addr, client_port)

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

        self.mensagem_codificada = self.CamadaFisica.encode(self.after_hamming)
        self.mensagem_modulada = self.CamadaFisica.modulate(self.after_hamming)

        # adicionar aqui logica para enviar mensagem para o socket, importante incluir mecanismo para mudar taxa de erro
        self.tranmissor.sendmsg(self.mensagem_codificada, int(self.Botao_enviar.InputProbErro.text()))

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