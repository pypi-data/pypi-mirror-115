#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import timeit


class Timer:
    def __init__(self):
        self.elapsed_time = 0
        self.__start = None
        self.__stop = None

        self.__running = False

    def start(self):
        assert not self.__running, "Timer is running. Stop it first before running it again."
        self.__running = True
        self.__start = timeit.default_timer()

    def stop(self):
        assert self.__running, "Timer is not running. Start it first before ending it."
        self.__end = timeit.default_timer()
        self.elapsed_time += self.__end - self.__start
        self.__running = False

    def reset(self):
        self.elapsed_time = 0

    def timeit(self, fn):
        def wrapper(*args, **kwargs):
            self.start()
            fn(*args, **kwargs)
            self.stop()

        return wrapper()
