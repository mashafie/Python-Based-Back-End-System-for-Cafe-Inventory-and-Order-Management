from unittest.mock import patch
from general_funcs import *

@patch('builtins.input')
def test_get_menu_choice_valid_input(mock_input):
    # Simulate user input
    mock_input.return_value = "3\n"
    expected_output = 3
    
    assert get_menu_choice(1, 5) == expected_output

@patch('builtins.input')
def test_get_menu_choice_invalid_input(mock_input):
    # Simulate user input
    mock_input.side_effect = ["invalid\n", "2\n"]
    expected_output = 2
    
    assert get_menu_choice(1, 5) == expected_output

@patch('builtins.input')
def test_get_menu_choice_out_of_range(mock_input):
    # Simulate user input
    mock_input.side_effect = ["6\n", "2\n"]
    expected_output = 2
    
    assert get_menu_choice(1, 5) == expected_output
