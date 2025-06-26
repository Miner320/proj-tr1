
import math

def decimalToBinary(dec_number):
    """!
    Função para converter números reais em bytes
    @param numero_decimal número real
    \retval numero_binario: o equivalente binário do número decimal, com 8 bits
    """

    result = ""
    for i in range(0,8):
        result = str(dec_number & 1) + result
        dec_number = dec_number >> 1
    return result

def binaryToDecimal(bin_string):
    """!
    Função que converte bytes em números reais
    @param byte string binária contendo 8 bits
    \retval decimal_num: número real
    """

    result = 0

    potencia = 128
    for i in bin_string:
        if(i == '1'):
            result = result + potencia
        potencia = potencia >> 1
    
    return result

class Hamming():

    def __numberOfParityBits(self, m):
        """!
        Esta função retorna o número de bits de paridade (r) necessários para codificar um string de tamanho m
        """

        for r in range(0,m):
            if(2**r >= m + r + 1):
                return r

            
    def __positionParityBits(self, message, r):
        """!
        Esta função posiciona os bits de paridade em uma string, colocando o caractere '-' nas posições necessárias
        """

        top_of_message = 0
        m = len(message)
        result_string = ""

        for i in range(1, m+r+1):
            if(math.log2(i).is_integer()):
                result_string = result_string + "-"
            else:
                result_string = result_string + message[top_of_message]
                top_of_message = top_of_message + 1

        return result_string
    
    def removeParityBits(self, message):
        """!
        Função que remove os bits de paridade de uma string binária 
        @param bit_string string binária
        @return string binária inserida sem os bits de paridade
        """

        result_string = ""
        posicao = 1

        for i in message:
            if(not(math.log2(posicao).is_integer())):
                result_string = result_string + i
            posicao = posicao + 1
        
        return result_string
        

    def __calcNthParityBit(self, bit_string):
        """!
        Esta função determina o valor do primeiro bit de paridade encontrado na bit_string, representado pelo caractere '-'
        """


        contador = 0
        nthBit = bit_string.find('-')+1
        for i in range(nthBit-1, len(bit_string)):
            if(i+1 & nthBit):
                if(bit_string[i]=='1'):
                    contador +=1

        if( (contador&1) == 0 ):
            return '0'
        else:
            return '1'
        
    def hammingEncode(self, bit_string):
        """!
        Função que faz codificação Hamming de uma string binária
        @param string string que passará por codificação
        @return string com bits de paridade
        """

        n_parity_bits = self.__numberOfParityBits(len(bit_string))
        bit_string = self.__positionParityBits(bit_string, n_parity_bits)

        while(bit_string.count('-') > 0):
            bit_string = bit_string.replace('-', self.__calcNthParityBit(bit_string),1)

        return bit_string

    def detectError(self, bit_string): #caso retorne 0 não houve erro, retorna a posição do erro caso contrário(começando contagem do array a partir de 1)
        """!
        Função que faz detecção de erros por codificação Hamming
        @param string string binária que passará por detecção de erros
        @return posição do bit em que ocorreu o erro, retorna 0 caso não haja erro
        """

        new_parity_bits= list()
        potencia = 1
        while(potencia < len(bit_string)):
            bit_inicio = bit_string[potencia-1]
            for i in range(potencia, len(bit_string)):
                if(i+1 & potencia):
                    if(bit_string[i]!=bit_inicio):
                        bit_inicio = '1'
                    else:
                        bit_inicio = '0'
            new_parity_bits.append(bit_inicio)
            potencia = potencia*2
        
        posicao_erro = 0
        potencia = 1
        for i in new_parity_bits:
            if(i=='1'):
                posicao_erro = posicao_erro + potencia
            potencia = potencia*2

        return posicao_erro
            
class CRCMachine():

    def __init__(self):
        """!
        Construtor que inicializa a instância com o polinômio crc32
        """

        self.polynomial = "100000100110000010001110110110111"

    def __crcXor(self, x, y):
        """!
        Esta função faz uma operação XOR entre 2 strings binárias, com exceção do bit mais significativo
        """

        if(len(x)<len(y)):
            limit = len(x)
        else:
            limit = len(y)
        
        result = ""
        for i in range(1, limit):
            if(x[i] == y[i]):
                result = result + '0'
            else:
                result = result + '1'
        return result
    
    def crcDivision(self, message):
        """!
        Função que faz a divisão de uma string binária pelo polinômio crc definido na instância da classe CRCMachine
        @param bit_string string binária
        \retval remainder: resto da divisão de bit_string pelo polinômio crc
        """

        limit = len(message)
        slice = len(self.polynomial)
        temp = message[0:slice]

        while(slice<limit):
            if(temp[0]=='1'):
                temp = self.__crcXor(temp, self.polynomial)
            else:
                temp = self.__crcXor("".zfill(slice), temp)
            temp = temp + message[slice]
            slice = slice + 1

        if(temp[0]=='1'):   
            temp = self.__crcXor(message, temp)
        else:
            temp = self.__crcXor("".zfill(slice), temp)
        return temp
            
    def crcRemainder(self, message):
        """!
        Função que retorna o resto da divisão por polinômio crc à uma string binária, após adição de 31 zeros à string inserida
        @param bit_string string binária
        \retval remainder: resto da divisão da string modificada pelo polinômio crc
        """
        
        temp = message+"".zfill(len(self.polynomial)-1)
        remainder = self.crcDivision(temp)
        return remainder

    def verifyCrc(self, message):
        """!
        Função que faz verificação de erros em uma mensagem usando o protocolo crc
        @param message mensagem na qual se deseja fazer verificação de erros
        \retval "erro crc" caso erro seja detectado
        \retval "ok" caso nenhum erro seja detectado
        """

        remainder = self.crcDivision(message)
        if('1' in remainder):
            return "erro crc"
        else:
            return "ok"
        
    def removeCrc(self, message):
        """!
        Função que de uma string o resto da divisão pelo polinômio crc
        @param message string binária
        @return string inserida sem o resto da divisão pelo polinômio
        """
        return message[0:len(message)-32]

class CamadaEnlace():
    
    def __init__(self):
        """!
        Construtor que inicia uma instância com os atributos necessários
        """
        self.flag_byte_insertion = "01111110"
        self.escape_flag_byte_insertion = "01111101"
        self.__crc_machine = CRCMachine()
        self.__hamming_encoder = Hamming()

    def messageToBits(self, message):
        """!
        Função que transforma uma string em seu equivalente binário seguindo a tabela ASCII
        @param mensagem string de caracteres
        @return string binária equivalente á string de caracteres inserida, seguindo a tabela ASCII
        """

        temp = "".join("0{0:8b}".format(ord(x), 'b')for x in message)
        return temp.replace(' ', '')
    
    def contagemCaracteres(self, bit_string):
        """!
        Função que adiciona um cabeçalho à uma string de bytes, representando o número de bytes na string
        @param bit_string string binária com um número inteiro de bytes
        @return string binária com um cabeçalho que representa o número de bytes na string
        """

        n_bytes = len(bit_string)//8
        byte_to_append = decimalToBinary(n_bytes)

        return byte_to_append + bit_string

    def __getQuadroContagemCaracteres(self, message):
        if (len(message)%8!=0):
            raise Exception("erro - contagem de caracteres comm fraçao de bytes")
        
        num_bytes = binaryToDecimal(message[0:8])

        temp = message[8:]
        remaning_bytes = len(temp)/8

        if(remaning_bytes < num_bytes):
            raise Exception("erro - contagem de caracteres errada")

        return temp[0:8*num_bytes]
    
    def separaQuadrosContagemCaracteres(self, message):
        """!
        Função que separa quadros demarcados por contagem de caracteres
        @param bit_string string binária
        @return lista com os quadros delimitados
        \throw Exception("erro - contagem de caracteres comm fraçao de bytes") caso não haja número inteiro de bytes
        \throw Exception("erro - contagem de caracteres errada") caso contagem de caracteres não seja condizente com o número de bytes na bit_string
        """

        lista_quadros = []

        while(len(message)):
            temp = self.__getQuadroContagemCaracteres(message)
            message = message[8+len(temp):]
            lista_quadros.append(temp)
        return lista_quadros

    def flagsByteInsertion(self, bit_string):
        """!
        Função que realiza delimitação de quadros com inserção de byte
        @param bit_string string binária
        @return bit_string modifica pelas flags de escape e delimitação de quadro
        """

        return_string = self.flag_byte_insertion

        n_bytes_in_string = len(bit_string)//8

        for i in range(0, n_bytes_in_string):
            current_byte = bit_string[i*8:i*8+8]

            if(current_byte == self.escape_flag_byte_insertion):
                return_string = return_string + self.escape_flag_byte_insertion + self.escape_flag_byte_insertion

            elif(current_byte == self.flag_byte_insertion):
                return_string = return_string + self.escape_flag_byte_insertion + self.flag_byte_insertion

            else:
                return_string = return_string + current_byte

        return_string = return_string + self.flag_byte_insertion

        return(return_string)
    
    def __validaQuadroByteInsertion(self, message):

        return_string = ""

        num_bytes = len(message)//8
        previous_escape_flag = False

        for i in range(0, num_bytes):

            skip_byte = False
            temp = message[i*8:8+8*i]

            if(temp == self.escape_flag_byte_insertion):
                skip_byte=True
                if(previous_escape_flag):
                    return_string = return_string + temp
                else:
                    previous_escape_flag = True
            
            if(temp == self.flag_byte_insertion):
                skip_byte = True
                if(previous_escape_flag):
                    return_string = return_string
                else:
                    raise Exception("erro inserçao de bytes")
                
            if(not skip_byte):
                return_string = return_string + temp

        return return_string

    
    def separaQuadrosByteInsertion(self, message):
        """!
        Função que separa quadros delimitados por inserção de byte
        @param bit_string
        @return lista com os quadros separados e sem flags de escape e delimitação
        \throw Exception("erro - inserçao de bytes com fraçao de bytes") caso número de bytes não seja inteiro
        \throw Exception("erro - inserçao de bytes com fraçao de bytes") caso quadro não comece com flag
        \throw Exception("erro - nao termina com flag") caso quadro não termine com flag
        """


        if (len(message)%8 != 0):
            raise Exception("erro - inserçao de bytes com fraçao de bytes")
        
        if ( message[0:8] != self.flag_byte_insertion ):
            raise Exception("erro - nao começa com flag")
        
        if ( message[-8:] != self.flag_byte_insertion ):
            raise Exception("erro - nao termina com flag")
        
        quadros = message.split(self.flag_byte_insertion*2)
        quadros[0] = quadros[0][8:] #remove a flag de inicio do primeiro quadro
        quadros[-1] = quadros[-1][:-8] #remove a flag final do ultimo quadro

        quadros = list(map(self.__validaQuadroByteInsertion, quadros))
        return quadros
 
    def flagsBitInsertion(self,bit_string):
        """!
        Função que faz delimitação de um quadro por inserção de bits
        @param bit_string string binária
        @return bit_string modifica pela flag de inserção de bits
        """


        flag = self.flag_byte_insertion
        temp_string = ""
        counter_1 = 0

        for i in bit_string:

            if(i=='1'):
                counter_1+=1

                if(counter_1==6):
                    temp_string = temp_string + '0'
                    temp_string = temp_string + '1'
                    counter_1 = 0
                else:
                    temp_string = temp_string + '1'

            else:
                temp_string = temp_string + '0'

        return(flag+temp_string+flag)
    
    def __validaQuadroBitInsertion(self,message):
        
        return_string = ""

        if(message.find(self.flag_byte_insertion) != -1 ):
            raise Exception("erro inserçao de bits - flag encontrada em quadro")
        
        message = message.replace("01111101",self.flag_byte_insertion)
        
        return message
    
    def separaQuadrosBitInsertion(self, message):
        """!
        Função que separa quadros delimitados por inserção de bits
        @param bit_string string binária
        @return lista de quadros sem a flag de inserção de bits
        \throw Exception("erro inserçao de bits - flag encontrada em quadro") caso flag seja encontrada dentro de um quadro
        \throw Exception("erro - nao começa com flag") caso string não comece com flag
        \throw Exception("erro - nao termina com flag") caso string não termine com flag
        """

        if ( message[0:8] != self.flag_byte_insertion ):
            raise Exception("erro - nao começa com flag")
        
        if ( message[-8:] != self.flag_byte_insertion ):
            raise Exception("erro - nao termina com flag")
        
        quadros = message.split(self.flag_byte_insertion*2)
        quadros[0] = quadros[0][8:] #remove a flag de inicio do primeiro quadro
        quadros[-1] = quadros[-1][:-8] #remove a flag final do ultimo quadro

        quadros = list(map(self.__validaQuadroBitInsertion, quadros))
        return quadros

    def crc32Encode(self, message):
        """!
        Função que adiciona o resto da divisão pelo polinômio crc32 à uma mensagem
        @param bit_string string binária
        @return string binária com o resto da divisão pelo polinômio crc concatenado à direita
        """

        remainder = self.__crc_machine.crcEncode(message)
        return message+remainder
    
    
    def paridadePar(self, bit_string):
        """!
        Função que adiciona um bit de paridade par à uma string binária
        @param bit_string string binária
        @return bit_string com o bit de paridade par adicionado à direita
        """
        temp_string = ""

        if(bit_string.count('1')%2==0):
            bit_paridade = '0'
        else:
            bit_paridade = '1'

        temp_string = bit_string + bit_paridade
        return temp_string
    
    def verificaParidadePar(self, bit_string):
        """!
        Função que verifica erros usando o bit de paridade em uma string binária
        @param bit_string string binária
        \retval "erro - bit de paridade" caso haja erro de bit de paridade
        \retval "ok" caso não haja erro
        """
        
        if( (bit_string.count('1')&1) == 0):
            return "ok"
        else:
            return "erro - bit de paridade"
        
    def removeBitParidade(self, bit_string):
        """!
        Função que retira o bit de paridade de uma string binária
        @param bit_string string binária
        @return string binária sem o bit menos significativo
        """

        return bit_string[0:len(bit_string)-1]



camada = CamadaEnlace()
msg = camada.flag_byte_insertion + decimalToBinary(14) + camada.flag_byte_insertion + camada.flag_byte_insertion + decimalToBinary(128) + camada.flag_byte_insertion
quadros = camada.separaQuadrosByteInsertion(msg)
print(quadros)