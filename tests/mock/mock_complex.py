class Complex:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def run(self) -> dict:
        return {
            'a': self.a ** 2,
            'b': self.a ** 2,
        }


def test_complex_func(a: int, b: int):
    c = Complex(a, b)
    out = c.run()
    c2 = Complex(**out)
    return c2.run()
