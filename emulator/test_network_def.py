import MNetworkDef


def test_malloc():
    example = MNetworkDef.Memory(200, 10)

    example[55] = 100
    print("\n", example)

    adr = example.malloc(3)

    print(example)
    print(adr)