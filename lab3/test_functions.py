import pytest
from first import count_iterative, count_recursive
from second import iterative_xi, recursive_xi

# Тесты для подсчёта элементов в списке
@pytest.mark.parametrize("lst, expected", [
    ([], 0),
    ([1, [2, 3]], 4),
    (["x", "y", ["z"]], 4),
    ([1, 2, [3, 4, [5]]], 7),
    ([1, 2, 4, ["z", "x"]], 6),
])
def test_count_elements(lst, expected):
    assert count_iterative(lst) == expected
    assert count_recursive(lst) == expected

# Тесты для расчёта xi
@pytest.mark.parametrize("i, expected", [
    (1, 1),
    (2, -0.125),
    (3, 0.166667),
    (4, 0.104167),
    (5, 0.263889),
])
def test_xi(i, expected):
    assert round(recursive_xi(i), 6) == round(expected, 6)
    assert round(iterative_xi(i), 6) == round(expected, 6)
