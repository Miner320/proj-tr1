from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit
from camadaFisica import CamadaFisica
from camadaEnlace import CamadaEnlace


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
        self.Label = QLabel("Tamanho maximo de quadro")
        self.InputTamanhoQuadro = QLineEdit()
        self.BotaoEnviar = QPushButton("Enviar mensagem")

        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.InputTamanhoQuadro)
        self.Layout.addWidget(self.BotaoEnviar)

        self.setLayout(self.Layout)



class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("interface de transmissão")

        # opções iniciais de enquadramento e detecção de erro
        self.Enquadramento = "Contagem"
        self.ErrorDetection = "ParityBit"
        self.listaQuadros = list()

        # declaracao das camadas
        self.CamadaFisica = CamadaFisica()
        self.CamadaEnlace = CamadaEnlace()

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

        self.setLayout(v_layout)

    def NRZP_clicked(self):
        self.CamadaFisica.setModulacaoDigital("NRZP")

    def Bipolar_clicked(self):
        self.CamadaFisica.setModulacaoDigital("Bipolar")
        
    def Manchester_clicked(self):
        self.CamadaFisica.setModulacaoDigital("Manchester")

    def ASK_clicked(self):
        self.CamadaFisica.setModulacaoAnalogica("ASK")

    def FSK_clicked(self):
        self.CamadaFisica.setModulacaoAnalogica("FSK")

    def PSK_clicked(self):
        self.CamadaFisica.setModulacaoAnalogica("PSK")

    def Contagem_clicked(self):
        self.Enquadramento = "Contagem"
    
    def ByteInsertion_clicked(self):
        self.Enquadramento = "ByteInsertion"

    def BitInsertion_clicked(self):
        self.Enquadramento = "BitInsertion"

    def ParityBit_clicked(self):
        self.ErrorDetection = "ParityBit"

    def CRC_clicked(self):
        self.ErrorDetection = "CRC"

    def Enviar_clicked(self):
        self.listaQuadros = []
        self.msg_bits = self.CamadaEnlace.messageToBits(self.MessageLayout.Input.toPlainText())
        self.Mensagem_em_bytes.Text.setText(self.msg_bits)

        if(self.Enquadramento == "Contagem"):
            self.quadro = self.CamadaEnlace.contagemCaracteres(self.msg_bits)
        elif(self.Enquadramento == "ByteInsertion"):
            self.quadro = self.CamadaEnlace.flagsByteInsertion(self.msg_bits)
        elif(self.Enquadramento == "BitInsertion"):
            self.quadro = self.CamadaEnlace.flagsBitInsertion(self.msg_bits)

        self.Mensagem_enquadramento.Text.setText(self.quadro)

        if(self.ErrorDetection == "ParityBit"):
            self.after_error_detection = self.CamadaEnlace.paridadePar(self.quadro)
        elif(self.ErrorDetection == "CRC"):
            self.after_error_detection = self.CamadaEnlace.crc32Encode(self.quadro)

        self.Mensagem_error_detection.Text.setText(self.after_error_detection)

        self.after_hamming = self.CamadaEnlace.hamming_encoder.hammingEncode(self.after_error_detection)

        self.Mensagem_hamming.Text.setText(self.after_hamming)
        
        