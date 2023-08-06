try:
    import xmltodict
except:
    raise ImportError('Unable to import xmltodict, please `pip install xmltodict==0.12.0`.')
else:
    if xmltodict.__version__ != '0.12.0':
        raise ImportError("xmltodict's version must be `0.12.0`, please `pip install xmltodict==0.12.0`.")
