import unittest

from pyx12.decorators import memoize, memoized


class TestMemoize(unittest.TestCase):
    def test_caches_result(self):
        call_count = [0]

        @memoize
        def add(a, b):
            call_count[0] += 1
            return a + b

        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(call_count[0], 1)

    def test_different_args_called_separately(self):
        call_count = [0]

        @memoize
        def add(a, b):
            call_count[0] += 1
            return a + b

        add(1, 2)
        add(3, 4)
        self.assertEqual(call_count[0], 2)

    def test_with_kwargs(self):
        call_count = [0]

        @memoize
        def greet(name, greeting="hello"):
            call_count[0] += 1
            return f"{greeting} {name}"

        result = greet("world", greeting="hi")
        greet("world", greeting="hi")
        self.assertEqual(call_count[0], 1)
        self.assertEqual(result, "hi world")

    def test_cache_attribute_exists(self):
        @memoize
        def identity(x):
            return x

        identity(42)
        self.assertIn((42,), identity.cache)

    def test_returns_cached_value(self):
        results = [10, 20]
        idx = [0]

        @memoize
        def changing():
            val = results[idx[0]]
            idx[0] = min(idx[0] + 1, len(results) - 1)
            return val

        self.assertEqual(changing(), 10)
        self.assertEqual(changing(), 10)


class TestMemoized(unittest.TestCase):
    def test_caches_result(self):
        call_count = [0]

        @memoized
        def square(n):
            call_count[0] += 1
            return n * n

        self.assertEqual(square(5), 25)
        self.assertEqual(square(5), 25)
        self.assertEqual(call_count[0], 1)

    def test_different_args_called_separately(self):
        call_count = [0]

        @memoized
        def square(n):
            call_count[0] += 1
            return n * n

        square(2)
        square(3)
        self.assertEqual(call_count[0], 2)

    def test_repr_returns_docstring(self):
        @memoized
        def documented():
            """my docstring"""
            pass

        self.assertEqual(repr(documented), "my docstring")


if __name__ == "__main__":
    unittest.main()
