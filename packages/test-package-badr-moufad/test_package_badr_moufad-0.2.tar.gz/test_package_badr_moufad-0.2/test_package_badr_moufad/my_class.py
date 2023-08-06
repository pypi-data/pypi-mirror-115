from test_package_badr_moufad.my_functions import say_hello, say_joke


class Person:
    def __init__(self, username: str) -> None:
        self.username = username
        
    def greet(self) -> None:
        say_hello(self.username)

    def joke(self) -> None:
        say_joke()
        
