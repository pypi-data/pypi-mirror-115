from .manager import ChainManager

__all__ = [
    'parse',
    'parse_string',
]

ATTR_PREFIX = '@'
CDATA_KEY = '#text'
REAL_CDATA_KEY = 'text_'

def parse_string(
        xml_data: str
        , attr_prefix: str = ATTR_PREFIX
        , cdata_key: str = CDATA_KEY
        , real_cdata_key: str = REAL_CDATA_KEY
    ):
    return ChainManager(
        xml_data
        , attr_prefix = attr_prefix
        , cdata_key = cdata_key
        , real_cdata_key = real_cdata_key
    )

def parse(
        path: str
        , attr_prefix: str = ATTR_PREFIX
        , cdata_key: str = CDATA_KEY
        , real_cdata_key: str = REAL_CDATA_KEY
        , encoding: str = 'utf-8'
    ):
    with open(path, 'r', encoding=encoding) as fp:
        xml_data = fp.read()

    return parse_string(
        xml_data
        , attr_prefix = attr_prefix
        , cdata_key = cdata_key
        , real_cdata_key = real_cdata_key
    )
