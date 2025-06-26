
import matplotlib.pyplot as plt
import numpy as np


class Encoder():
    """!
    Classe que faz codificação digital de strings binárias
    """

    def __NRZPEncoder(self, binaryString, voltageLevel):

        NRZPList = []
        for bit in binaryString:
            if(bit=='1'):
                NRZPList.append(voltageLevel)
            else:
                NRZPList.append(-voltageLevel)

        return NRZPList
    
    def __bipolarEncoder(self, binaryString, voltageLevel):

        bipolarList = []
        currentVoltage = voltageLevel

        for bit in binaryString:
            if(bit=='0'):
                bipolarList.append(0)
            else:
                bipolarList.append(currentVoltage)
                currentVoltage = -currentVoltage
        
        return bipolarList
    
    def __manchesterEncoder(self, binaryString):

        manchesterList = []
        
        for bit in binaryString:
            if(bit=='0'):
                manchesterList.append("01")
            else:
                manchesterList.append("10")

        return manchesterList

    def Encode(self, code, voltage, bit_train):
        """!
        Função que faz codificação digital de acordo com a codificação definida na instância da classe
        @param bit_string string binária
        @return lista com os símbolos elétricos determinados pela codificação escolhida, separa os símbolos por tempo de bit
        """

        return_list = []

        if(code == "NRZP"):
            return_list = self.__NRZPEncoder(bit_train, voltage)
        
        if(code == "Bipolar"):
            return_list = self.__bipolarEncoder(bit_train, voltage)

        if(code == "Manchester"):
            return_list = self.__manchesterEncoder(bit_train)

        return return_list
        
    

class Modulator():
    """!
    Classe que faz modulação analógica de uma string binária
    """

    def __FSK(self, bit_string, amplitude, base_frequency):

        return_signal = []

        for bit in bit_string:
            if(bit=='1'):
                for i in range(0,120):
                    return_signal.append( amplitude*np.sin(2*np.pi*2*base_frequency*i/120))
            else:
                for i in range(0,120):
                    return_signal.append( amplitude*np.sin(2*np.pi*base_frequency*i/120))

        return return_signal
    
    def __ASK(self, bit_string, base_amplitude, frequency):

        return_signal = []

        for bit in bit_string:
            if(bit=='1'):
                for i in range(0,120):
                    return_signal.append( base_amplitude*np.sin(2*np.pi*frequency*i/120))
            else:
                for i in range(0,120):
                    return_signal.append(0)

        return return_signal
    
    def __PSK(self, bit_string, amplitude, frequency):
        
        phase_dict = dict()
        phase_dict["000"] = 0
        phase_dict["001"] = np.pi/4
        phase_dict["010"] = np.pi/2
        phase_dict["011"] = 3*np.pi/4
        phase_dict["111"] = np.pi
        phase_dict["110"] = 5*np.pi/4
        phase_dict["101"] = 3*np.pi/2
        phase_dict["100"] = 7*np.pi/4

        return_signal = []
        temp_bts = bit_string

        while(len(temp_bts)%3 != 0):
            temp_bts = temp_bts + '0'

        index = 0
        while(index in range(0, len(temp_bts))):

            current_phase = phase_dict[temp_bts[index:index+3]]
            
            for i in range(0,120):
                return_signal.append(amplitude*np.sin(2*np.pi*frequency*i/40 + current_phase ))

            index = index + 3

        return return_signal
    
    def Modulate(self, modulation , bit_string, amplitude, frequency):
        """!
        Função que faz modulação analógica de acordo com a modulação definida na instância da classe
        @param bit_string string binária
        @return lista com os símbolos elétricos determinados pela modulação escolhida, separa os símbolos por tempo de bit
        """

        return_list = []

        if(modulation == "ASK"):
            return_list = self.__ASK(bit_string, amplitude, frequency)
        
        if(modulation == "FSK"):
            return_list = self.__FSK(bit_string, amplitude, frequency)

        if(modulation == "PSK"):
            return_list = self.__PSK(bit_string, amplitude, frequency)

        return return_list



class CamadaFisica():
    """!
    Classe que reúne as funções da camada física
    """


    def __init__(self):
        self.modulador = Modulator()
        self.codificador = Encoder()
        self.modulacao_digital = "NRZP"
        self.modulacao_analogica = "ASK"
        self.amplitude = 1
        self.frequency = 1

    def setModulacaoDigital(self, string):
        """!
        define a codificação digital (opções válidas: NRZP, Bipolar, Manchester)
        """
        self.modulacao_digital = string

    def setModulacaoAnalogica(self, string):
        """!
        define a modulação analógica (opções válidas: ASK, FSK, PSK)
        """
        self.modulacao_digital = string

    def setAmplitude(self, number):
        """!
        define a amplitude usada para codificação e modulação
        """
        self.amplitude = number

    def setFrequency(self, number):
        """!
        define a frequência usada para modulação analógica
        """
        self.frequency = number

    def modulate(self, bitString):
        """!
        Realiza modulação analógica de acordo com os parâmetros definidos por atributos da classe
        @param bit_string string binária
        @return lista com os símbolos elétricos determinados pela modulação escolhida, separa os símbolos por tempo de bit
        """

        return self.modulador.Modulate(self.modulacao_analogica, bitString, self.amplitude, self.frequency)

    def encode(self, bitString):
        """!
        Função que faz codificação digital de acordo com a codificação definida na instância da classe
        @param bit_string string binária
        @return lista com os símbolos elétricos determinados pela codificação escolhida, separa os símbolos por tempo de bit
        """

        return self.codificador.Encode(self.modulacao_digital, self.amplitude, bitString)
    
    def encodeSignal(self, bit_string):

        electric_symbols = self.encode(bit_string)
        return_signal = []
        
        if(self.modulacao_digital != "Manchester"):
            for symbol in electric_symbols:
                for sample in range(0,120):
                    return_signal.append(symbol)

        else:
            for symbol in electric_symbols:
                for sample in range(0,60):
                    return_signal.append(int(symbol[0]))
                for sample in range(0,60):
                    return_signal.append(int(symbol[1]))

        return return_signal



class GraphMaker():
    """!
    Classe que faz gráficos de sinais modulados ou codificados
    """

    def MakeModulatedGraph(self,modulatedArray):
        """!
        Função que faz o gráfico de um sinal modulado e salva no arquivo "modulated.jpg"
        @param Array lista de símbolos elétricos de um sinal modulado
        """

        fig, ax = plt.subplots()
        x_axis = range(0, len(modulatedArray))
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Tensão")
        ax.set_title("Sinal Modulado")
        ax.grid(visible=True)
        ax.plot(x_axis, modulatedArray)
        plt.savefig("modulated.jpg")
        return

    def MakeEncodedGraph(self, encodedArray, bitTime):
        """!
        Função que faz o gráfico de um sinal codificado e salva no arquivo "encoded.jpg"
        @param Array lista de símbolos elétricos de um sinal codificado
        """
        fig, ax = plt.subplots()
        x_axis = range(0, len(encodedArray)*bitTime)

        temp_bits = []
        for value in encodedArray:
            for iterator in range(0, bitTime):
                temp_bits.append(value)

        ax.set_xlabel("Tempo")
        ax.set_ylabel("Tensão")
        ax.set_title("Sinal Modulado")
        ax.grid(visible=True)
        ax.plot(x_axis, temp_bits)
        plt.savefig("encoded.jpg")
        return

    def MakeManchesterGraph(self, manchesterArray, bitTime):
        """!
        Função que faz o gráfico de um sinal codificado usando codificação Manchester e salva no arquivo "manchester.jpg" "
        @param Array lista de símbolos elétricos de um sinal codificado
        """
        fig, ax = plt.subplots()
        x_axis = range(0, len(manchesterArray)*bitTime)

        temp_bits = []
        for value in manchesterArray:
            for iterator in range(0, bitTime//2):
                temp_bits.append(int(value[0]))
            for iterator in range(bitTime//2, bitTime):
                temp_bits.append(int(value[1]))
            
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Tensão")
        ax.set_title("Sinal Modulado")
        ax.grid(visible=True)
        ax.plot(x_axis, temp_bits)
        plt.savefig("manchester.jpg")
        return

bitString = "101"
signal = []

camada = CamadaFisica()

signal = camada.encodeSignal(bitString)
x_axis = range(0,len(signal))
plt.plot(x_axis,signal)
plt.show()