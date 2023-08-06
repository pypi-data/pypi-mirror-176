from typing import Any
from os import urandom
from datetime import datetime, timezone
from bitstring import ConstBitStream, ReadError

from .encryption import decrypt, encrypt
from .packet import D2LPacket, PacketType

from .crc import calculate

UINT16MAX = 65535

OFFSET_EPOCH = datetime(2016, 1, 1, tzinfo=timezone.utc)
OFFSET_ENCRYPTED = 16
OFFSET_PAYLOAD = 38

RES_HORLOGE_SIZE = 48


def _generate_response_get_horloge(packet: D2LPacket, payload: bytes) -> bytearray:
    '''
    Generate the response packet bytearray to send back to the D2L
    '''
    crc_pre = bytearray()
    crc_post = bytearray()

    crc_pre += (3).to_bytes(1, 'little')                # versionProtocole
    crc_pre += (0).to_bytes(1, 'little')                # Non Utilisee
    crc_pre += (RES_HORLOGE_SIZE).to_bytes(2, 'little')  # tailleTrame
    crc_pre += (packet.id_d2l).to_bytes(8, 'little')    # id D2L
    crc_pre += (0b00000001).to_bytes(1, 'little')       # Clef
    crc_pre += (0).to_bytes(3, 'little')                # Non Utilisee
    crc_pre += urandom(16)                              # nombreAleatoire

    crc_post += (4).to_bytes(2, 'little')           # taillePayload
    crc_post += (0b10000101).to_bytes(1, 'little')  # Requete/Reponse + typePayload
    crc_post += (0b00000000).to_bytes(1, 'little')  # commandSuivante/Erreur
    crc_post += (payload).to_bytes(4, 'little')     # Actual payload

    calc_bytes = crc_pre + crc_post
    crc16 = calculate(calc_bytes)
    crc_pre += (crc16).to_bytes(2, 'little')        # CRC16

    response = crc_pre + crc_post
    response = response.ljust(RES_HORLOGE_SIZE, b'\x00')    # Set block size to tailleTrame

    return response


class D2LParser:
    last_packet = None
    prev_packet = None

    def __init__(self, d2l_key: str, d2l_iv: str) -> None:
        self.d2l_key = bytes.fromhex(d2l_key)
        self.d2l_iv = bytes.fromhex(d2l_iv)

    def get_last_packet(self) -> D2LPacket:
        return self.last_packet

    def get_previous_packet(self) -> D2LPacket:
        return self.prev_packet

    def parse_request(self, msg: bytes, encrypted: bool = True) -> D2LPacket:
        '''
        Return a Packet which contains a header and payload dict with all data
        '''

        if encrypted:
            msg_decr = self._decrypt(msg)
        else:
            msg_decr = msg

        header = self._parse_header(msg_decr)
        payload = self._parse_payload(msg_decr, header["taillePayload"])

        return D2LPacket(header, payload, msg_decr)

    def generate_response(self, packet: D2LPacket, encrypted: bool = True) -> bytearray:
        '''
        Generate the response for a parsed D2LPacket
        '''
        assert packet.packet_type

        response = None

        if packet.packet_type == PacketType.GET_FIRMWARE:
            raise NotImplementedError
        if packet.packet_type == PacketType.GET_HORLOGE:
            payload = int((datetime.now(tz=timezone.utc) - OFFSET_EPOCH).total_seconds())
            response = _generate_response_get_horloge(packet, payload)
        if packet.packet_type == PacketType.PUSH_JSON:
            raise NotImplementedError

        if encrypted:
            response = self._encrypt(response)

        return response

    def _parse_header(self, message: bytes) -> dict:
        result = {}
        bitstream = ConstBitStream(message)
        try:
            result["versionProtocole"] = bitstream.read('uint:8')
            bitstream.read(8)           # Unused
            result["tailleTrame"] = bitstream.read('uintle:16')
            result["idD2L"] = bitstream.read('uintle:64')
            bitstream.read('bits:5')    # Unused
            result["clef"] = bitstream.read('bits:3').uint
            bitstream.read(24)          # Unused
            result["nombreAleatoire"] = bitstream.read('uintle:128')
            result["CRC16"] = bitstream.read('uintle:16')
            result["taillePayload"] = bitstream.read('uintle:16')
            result["isRequeteOuReponse"] = bitstream.read('bool:1')
            result["typePayload"] = PacketType(bitstream.read('bits:7').uint)
            result["isErreurTraitement"] = bitstream.read('bool:1')
            result["commandeSuivante"] = bitstream.read('bits:7').uint
        except ReadError as error:
            print(f"Failed to parse header: {bitstream}")
            raise error
        return result

    def _parse_payload(self, msg: bytes, msg_len: int) -> Any:
        result = None
        if msg_len <= 0:
            print("No payload to be parsed")
            return result
        payload = msg[OFFSET_PAYLOAD:OFFSET_PAYLOAD+msg_len]
        return payload

    def _decrypt(self, msg_encrypted: bytes) -> bytes:
        message_done = msg_encrypted[:OFFSET_ENCRYPTED]
        message_todo = msg_encrypted[OFFSET_ENCRYPTED:]
        message_todo = decrypt(message_todo, self.d2l_key, self.d2l_iv)
        return message_done + message_todo

    def _encrypt(self, msg_decrypted: bytes) -> bytes:
        message_done = msg_decrypted[:OFFSET_ENCRYPTED]
        message_todo = msg_decrypted[OFFSET_ENCRYPTED:]
        message_todo = encrypt(message_todo, self.d2l_key, self.d2l_iv)
        return message_done + message_todo
