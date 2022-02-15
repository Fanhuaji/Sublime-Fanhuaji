import sys

try:
    from .. import chardet
except ImportError:
    from .. import charset_normalizer as chardet
    import warnings

    warnings.filterwarnings('ignore', 'Trying to detect', module='charset_normalizer')
