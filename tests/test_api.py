
def test_leq(nsrt):
    leq = nsrt.read_leq()

    print(f'leq: {leq}')

    assert 30 < leq < 60


def test_temperature(nsrt):
    temperature = nsrt.read_temperature()

    print(f'temperature: {temperature}')

    assert 10 < temperature < 30
