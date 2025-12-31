import base64
from NeditGD.Dictionaries.PropertyID import NAME_TO_ID
from NeditGD.Dictionaries.PropertyHSV import HSV
from NeditGD.Dictionaries.ParticleEmitter import Emitter

# Define decoding functions first

# Decode a list encoded RobTop's way
def decode_list(data: str) -> list[int]:
    if not data: return []
    return list(map(int, data.split('.')))

# Encode a list RobTop's way
def encode_list(p_id: int, data: list[int]) -> str:
    if not data:
        return ''
    str_list = '.'.join(map(str, data))
    return f'{p_id},{str_list},'

def decode_pairs_list(data: str) -> list[tuple]:
    l = decode_list(data)
    return list(zip(l[::2], l[1::2]))

def encode_pairs_list(p_id: int, data: list[tuple[int]]) -> str:
    if not data:
        return ''
    
    str_list = '.'.join([f'{p[0]}.{p[1]}' for p in data])
    return f'{p_id},{str_list},'


def decode_HSV(data: str) -> HSV:
    values = map(float, data.split('a'))
    return HSV(*values)

def encode_HSV(p_id: int, hsv: HSV) -> str:
    hsv_enc = 'a'.join(map(str, hsv.get_property_list()))
    return f'{p_id},{hsv_enc},'

# The text object's message is encoded in base64, this method decodes it.
def decode_text(data: bytes) -> str:
    return base64.b64decode(data, altchars=b'-_').decode()

# The text object's message is encoded in base64,
# this method encodes plaintext.
def encode_text(p_id: int, text: str) -> str:
    enc = base64.b64encode(text.encode()).decode()
    enc = base64.b64encode(text.encode(), altchars=b'-_').decode()
    return f'{p_id},{enc},'

# Pre-calculate sets for faster lookup
_GROUPS_IDS = {NAME_TO_ID['groups'], NAME_TO_ID['parent_groups'], NAME_TO_ID['events']}
_PAIRS_LIST_IDS = {NAME_TO_ID['spawn_remap'], NAME_TO_ID['group_probabilities'], NAME_TO_ID['sequence']}
_HSV_IDS = {NAME_TO_ID['hsv'], NAME_TO_ID['color_2_hsv'], NAME_TO_ID['copied_color_hsv']}
_TEXT_ID = NAME_TO_ID['text']
_PARTICLE_SETUP_ID = NAME_TO_ID['particle_setup']

# Dispatch table for special property types
_SPECIAL_DECODERS = {}
for _id in _GROUPS_IDS:
    _SPECIAL_DECODERS[_id] = decode_list
for _id in _PAIRS_LIST_IDS:
    _SPECIAL_DECODERS[_id] = decode_pairs_list
for _id in _HSV_IDS:
    _SPECIAL_DECODERS[_id] = decode_HSV
_SPECIAL_DECODERS[_TEXT_ID] = decode_text


# Decode a property encoded RobTop's way
def decode_property_pair(p_id: int, data: str) -> int | float | list[int]:
    # Check special decoders first using the dispatch table
    decoder = _SPECIAL_DECODERS.get(p_id)
    if decoder:
        return decoder(data)

    if p_id == _PARTICLE_SETUP_ID:
        return data

    # Fast path for numbers
    # Most properties are integers. Try int conversion first.
    try:
        return int(data)
    except ValueError:
        pass

    # If int failed, try float
    try:
        return float(data)
    except ValueError:
        pass

    try:
        return base64.b64decode(data, altchars=b'-_')
    except:
        raise Exception(
            '[Nedit]: Unknown property declaration', p_id, data)

# Encode a property RobTop's way
def encode_property(p_id: int, data: str) -> str:
    if type(data) is list:
        if data and type(data[0]) is tuple:
            return encode_pairs_list(p_id, data)
        return encode_list(p_id, data)

    if p_id == NAME_TO_ID['particle_setup']:
        return f'{p_id},{data},'

    if type(data) is str:
        return encode_text(p_id, data)

    if type(data) is HSV:
        return encode_HSV(p_id, data)

    return f'{p_id},{data},'

# Get the name of a property if one exists,
# else get ID with leading underscore
def get_property_name(p_id: int):
    key_str = f'_{p_id}'
    for name, _id in NAME_TO_ID.items():
        if _id == p_id:
            key_str = name
            break
    return key_str
