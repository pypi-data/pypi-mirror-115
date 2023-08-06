def say_hello(name: str = None) -> str:
    return "Hello!" if name is None else f"Hello {name}!"
