import pytest
from rpn_calculator import RPNCalculator, RPNSyntaxError


@pytest.fixture
def calculator():
    return RPNCalculator()


def test_simple_expressions(calculator):
    assert calculator.evaluate("2 + 2") == 4
    assert calculator.evaluate("5 - 3") == 2
    assert calculator.evaluate("4 * 3") == 12
    assert calculator.evaluate("10 / 2") == 5


def test_operator_priority(calculator):
    assert calculator.evaluate("2 + 2 * 2") == 6
    assert calculator.evaluate("(2 + 2) * 2") == 8
    assert calculator.evaluate("10 - 4 / 2") == 8
    assert calculator.evaluate("(10 - 4) / 2") == 3


def test_float_numbers(calculator):
    assert calculator.evaluate("2.5 + 2.5") == 5
    assert calculator.evaluate("10 / 4") == 2.5
    assert calculator.evaluate("0.1 + 0.2") == pytest.approx(0.3)


def test_complex_expressions(calculator):
    assert calculator.evaluate("(5 + 3) * (10 - 4) / 2") == 24
    assert calculator.evaluate("10 + 2 * 3 - 4 / 2") == 14
    assert calculator.evaluate("( ( 15 / ( 7 - ( 1 + 1 ) ) ) * 3 ) - ( 2 + ( 1 + 1 ) )") == 5


def test_division_by_zero(calculator):
    with pytest.raises(ValueError, match="Деление на ноль"):
        calculator.evaluate("10 / 0")


def test_syntax_errors(calculator):
    with pytest.raises(RPNSyntaxError):
        calculator.evaluate("")
    with pytest.raises(RPNSyntaxError):
        calculator.evaluate("2 + + 2")
    with pytest.raises(RPNSyntaxError):
        calculator.evaluate("(2 + 2")
    with pytest.raises(RPNSyntaxError):
        calculator.evaluate("2 + 2)")
    with pytest.raises(RPNSyntaxError):
        calculator.evaluate("2 $ 2")


def test_rpn_conversion(calculator):
    assert calculator.parse_expression("3 + 4") == [3, 4, '+']
    assert calculator.parse_expression("3 + 4 * 5") == [3, 4, 5, '*', '+']
    assert calculator.parse_expression("(3 + 4) * 5") == [3, 4, '+', 5, '*']
    assert calculator.parse_expression("( 5 + 3 ) * ( 10 - 4 ) / 2") == [5, 3, '+', 10, 4, '-', '*', 2, '/']
