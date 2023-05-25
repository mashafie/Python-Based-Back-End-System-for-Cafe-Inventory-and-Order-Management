from unittest.mock import patch, Mock
from products_module import add_new_product

@patch("builtins.input")
def test_add_new_product_successful(mock_input):
    mock_input.side_effect = ["Product 1", "10.0", "0"]
    with patch("products_module.save_new_product") as mock_save:
        add_new_product()
        mock_save.assert_called_once_with({"name": "Product 1", "price": 10.0})

@patch("builtins.input")
def test_add_new_product_invalid_price(mock_input):
    mock_input.side_effect = ["Product 2", "invalid price", "10.0", "0"]
    with patch("products_module.save_new_product") as mock_save:
        add_new_product()
        mock_save.assert_called_once_with({"name": "Product 2", "price": 10.0})


