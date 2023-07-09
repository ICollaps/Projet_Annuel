# pytest tests/test_converts.py
from utils.functions import convert_numpy_int64
import numpy as np

def test_convert_numpy_int64():
    # Creating a dictionary with np.int64, regular int, and other types
    document = {
        'np_int': np.int64(1),
        'regular_int': 2,
        'float': 3.0,
        'str': 'test',
    }

    # Convert np.int64 to regular int
    converted_document = convert_numpy_int64(document)

    # Assert that np.int64 is converted to regular int
    assert isinstance(converted_document['np_int'], int)

    # Assert that regular int is still int
    assert isinstance(converted_document['regular_int'], int)

    # Assert that other types are unchanged
    assert isinstance(converted_document['float'], float)
    assert isinstance(converted_document['str'], str)
