import NetworkDef


def test_malloc():
    example = NetworkDef.Memory(200, 10)
    print("\n",example)

    example[55]=100
    adr=example.malloc(3)
    print(adr)
    print(example)