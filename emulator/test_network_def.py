
import pytest
import NetworkDef as Network
def test_malloc():
    example=Network.Memory(100, 10)
    print(example)
    assert example.sreg(10)
