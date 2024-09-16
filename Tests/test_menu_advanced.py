from menux.generator import MenuBuilder
from unittest.mock import patch

import pytest

def add():
    n1 = int(input())
    n2 = int(input())
    return n1 + n2

def sub():
    n1 = int(input())
    n2 = int(input())
    return n1 - n2

@pytest.fixture
def setup_menu_builder():
    builder = MenuBuilder()

    builder.add(
        "main",
        {1: "Add", 2: "More"},
        {1: add, 2: None},
        None
    )

    builder.add_submenu(
        "main",
        2,
        "main-sub",
        {1: "sub"},
        {1: sub},
        None,
        True,
    )

    return builder

def test_menu_print_and_sub_menu(capsys, setup_menu_builder):
    menu = setup_menu_builder

    with patch('builtins.input', side_effect=['2', '1', '40', '10']):
        result = menu.handler("Enter: ", return_execution_result=True)

        captured = capsys.readouterr()

        assert "1 - Add" in captured.out
        assert "3 - Go back" in captured.out
        assert "1 - sub" in captured.out
        assert result == (True, 30)

def test_menu_go_back(capsys, setup_menu_builder):
    menu = setup_menu_builder

    with patch('builtins.input', side_effect=['2', '2', '1', '10', '10']):
        result = menu.handler("Enter: ", return_execution_result=True)

        captured = capsys.readouterr()

        count = 0
        for line in captured.out.splitlines():
            if "1 - Add" in line:
                count += 1
        
        assert count == 2
        assert result == (True, 20)