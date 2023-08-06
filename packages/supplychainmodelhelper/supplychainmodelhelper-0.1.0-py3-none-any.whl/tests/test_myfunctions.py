from playground import supplychainmodulator as pg

def test_haversine():
    assert pg.haversine(52.370216, 4.895168, 52.520008,13.404954) == 945793.4375088713
