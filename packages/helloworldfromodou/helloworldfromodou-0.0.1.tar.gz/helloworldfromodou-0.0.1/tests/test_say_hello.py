from helloworldfromodou import say_hello


def test_response():
    grettings = say_hello('modou')
    assert grettings == 'Hello, modou!'