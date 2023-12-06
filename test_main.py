"""
Test goes here

"""

from main import add


def test_add_positive_numbers():
    assert add(1, 3) == 4


def test_add_negative_numbers():
    assert add(-2, -4) == -6


def test_add_mixed_numbers():
    assert add(7, -5) == 2


if __name__ == "__main__":
    test_add_positive_numbers()
    test_add_negative_numbers()
    test_add_mixed_numbers()
    print("All tests passed.")
