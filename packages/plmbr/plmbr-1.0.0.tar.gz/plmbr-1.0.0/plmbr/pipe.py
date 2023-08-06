from abc import abstractmethod
from typing import Iterator


class Tap:
    def __init__(self, action):
        self.action = action

    def __sub__(self, p):
        return Tap(lambda: p(self()))

    def __gt__(self, p):
        for _ in (self - p)():
            pass

    def __call__(self):
        return self.action()


class Pipe:
    def __sub__(self, p):
        return pipe(lambda it: p(self(it)))

    def __rsub__(self, it):
        return Tap(lambda: self(it))

    def __lt__(self, it):
        Tap(self) > (lambda it: it)

    def __call__(self, it):
        return self.pipe(it)

    @abstractmethod
    def pipe(self, it: Iterator) -> Iterator: ...


class pipe(Pipe):
    def __init__(self, action):
        self.action = action

    def pipe(self, it):
        return self.action(it)
