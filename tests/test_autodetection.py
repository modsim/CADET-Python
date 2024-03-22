from cadet import Cadet


def test_autodetection():
    sim = Cadet()
    assert sim.cadet_runner is not None
