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
