import NetworkDef


def test_malloc():
    example = NetworkDef.Memory(200, 10)

    example[55] = 100
    print("\n", example)

    adr = example.malloc(1)
    print(adr)
    print(example)