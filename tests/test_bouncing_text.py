import pytest

import bouncing_text


@pytest.mark.parametrize("argument, expected_result", [
    ([], "Text Here"), (["Test Message"], "Test Message"),
    (["DVD"], "DVD"),
]
)
def test_argument_parser_custom_text(argument, expected_result):
    result = bouncing_text.argument_parser(argument)
    assert result.text == expected_result


@pytest.mark.parametrize("arguments, expected_result", [
    ([], 5), (["-s", "2"], 2), (["--speed", "8"], 8)
])
def test_argument_parser_set_speed(arguments, expected_result):
    result = bouncing_text.argument_parser(arguments)
    assert result.speed == expected_result


@pytest.mark.parametrize("test_arguments", [
    ["-s", "20"], ["--speed", "-20"], ["--speed", "-6"], ["-s", "test"],
    ["-s", "5.5"], ["-s", "-6.2"], ["-s", "5 5"],
])
def test_argument_parser_set_speed_error(test_arguments):
    with pytest.raises(SystemExit):
        bouncing_text.argument_parser(test_arguments)


@pytest.mark.parametrize("test_values, expected_results", [
    ("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4),
    ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9)
])
def test_positive_int_zero_to_nine_normal(test_values, expected_results):
    result = bouncing_text.positive_int_zero_to_nine(test_values)
    assert result == expected_results


@pytest.mark.parametrize("test_values", [
    "-5", "10", "100", "2.5", " ", "Test", "test&*#", "", " 125445244545"
])
def test_positive_int_zero_to_nine_error(test_values):
    with pytest.raises(bouncing_text.argparse.ArgumentTypeError):
        bouncing_text.positive_int_zero_to_nine(test_values)
