import pytest


@pytest.mark.parametrize(
    "inp,expected",
    [
        (1, 2),
        (0, 1),
        (5, 6),
    ],
)
def test_increment_example(inp, expected):
    # Reemplaza esta función por la llamada real a tu lógica
    got = inp + 1
    assert got == expected
