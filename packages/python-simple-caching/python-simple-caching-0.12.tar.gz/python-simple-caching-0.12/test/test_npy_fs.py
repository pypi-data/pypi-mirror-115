from simple_caching import NpyFS

class TestNpyFS:
    def test_npyfs_1(self):
        cache = NpyFS()
        assert not cache is None

    def test_npyfs_2(self):
        cache = NpyFS()
        assert cache.check("hi") == False
        try:
            _ = cacge.get("hi")
            assert False
        except Exception:
            pass
        cache.set("hi", 3)
        assert cache.check("hi") == True
        assert cache.get("hi") == 3