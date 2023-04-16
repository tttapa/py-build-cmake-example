from py_build_cmake_example.add_module import add


def test_add():
    assert add(1, 2) == 3


from py_build_cmake_example import __version__ as py_version
from py_build_cmake_example.add_module import __version__ as py_cpp_version
from py_build_cmake_example._add_module import __version__ as cpp_version


def test_version():
    assert py_version == py_cpp_version
    assert py_version == cpp_version
    try: # No importlib in Python 3.7 and below
        from importlib.metadata import version
        assert py_version == version('py_build_cmake_example')
    except ImportError:
        pass
