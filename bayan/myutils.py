# Simple Python module to be imported from Bayan (placed at package root for easy import)

def hello(name: str) -> str:
    return f"Hello from Python, {name}!"


def fib(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

