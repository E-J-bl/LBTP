
import NetworkDef
def test_malloc():
    example =NetworkDef.Memory(100, 10)
    print(example)
    assert example.sreg==10
    adre1=example.malloc(3)
    print(example)