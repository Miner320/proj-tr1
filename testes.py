from camadaEnlace import CamadaEnlace

message = "10100110"
camada = CamadaEnlace()
msg_after_crc = camada.crc32Encode(message)

msg = "01111110011000010111111000110101011001001101000000100001"
print(camada.crc32Verify(msg))