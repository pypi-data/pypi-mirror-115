from helloworldagain import say_hello

def test_say_hello_no_params():
    assert say_hello() == "Hello, world!"

def test_say_hello_with_params():
    assert say_hello("Everybody") == "Hello, Everybody!"