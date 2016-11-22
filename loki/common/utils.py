def make_mock_object(**kwargs):
    return type('', (object, ), kwargs)
