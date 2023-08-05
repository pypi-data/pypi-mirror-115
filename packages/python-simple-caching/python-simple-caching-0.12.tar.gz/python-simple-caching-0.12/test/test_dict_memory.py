from simple_caching import DictMemory

class TestDictMemory:
    def test_memorydict_1(self):
        cache = DictMemory()
        assert not cache is None

    def test_memorydict_2(self):
        cache = DictMemory()
        assert cache.check("hi") == False
        try:
            _ = cacge.get("hi")
            assert False
        except Exception:
            pass
        cache.set("hi", 3)
        assert cache.check("hi") == True
        assert cache.get("hi") == 3