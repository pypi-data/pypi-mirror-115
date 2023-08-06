
def say_hello(name: str=None) -> str:
    """[summary]

    Args:
        name (str, optional): [description]. Defaults to None.

    Returns:
        str: [description]
    """

    if name is None:
        return "Hello, world!"
    else:
           return f"Hello, {name}!"


