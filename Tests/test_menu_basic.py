from menux.simple import Menu
from unittest.mock import patch

import pytest

# demo functions
def add():
    n1 = int(input("enter n1: "))
    n2 = int(input("enter n2: "))
    return n1 + n2

def sub():
    n1 = int(input("enter n1: "))
    n2 = int(input("enter n2: "))
    return n1 - n2

@pytest.fixture
def setup_menu():
    menu = Menu("menu1", {1: "Add nums", 2: "subtract nums"}, {1: add, 2: sub}, None, None)
    return menu

def test_menu_print(capsys, setup_menu):
    menu = setup_menu

    with patch('builtins.input', side_effect=['1', '10', '20']):
        result = menu.handler("Enter your choice: ")

        captured = capsys.readouterr()

        assert "Menu: menu1" in captured.out
        assert "1 - Add nums" in captured.out
        assert "2 - subtract nums" in captured.out
        assert "3 - Go back" in captured.out
        assert "Menu Executed" in captured.out

def test_menu_result(capsys, setup_menu):
    menu = setup_menu

    with patch('builtins.input', side_effect=['1', '20', '20']):
        result = menu.handler("Enter: ", return_execution_result=True)
        assert result == (True, 40)

def test_menu_formatting(capsys, setup_menu):
    menu = setup_menu

    with patch('builtins.input', side_effect=['1', '20', '20']):
        result = menu.handler("Enter: ", Title_Format="{identifier}", Body_Format="{index}: {text}", return_execution_result=True)
        
        captured = capsys.readouterr()

        assert "menu1\n" in captured.out
        assert "1: Add nums" in captured.out
