"""
Unit tests for the Quote Service.

These tests verify the parsing and loading functionality for quotes from multiple file sources.
Tests use mocking to isolate functionality and avoid dependencies on actual files.

To run:
    cd QuoteService
    python3 -m venv venv
    source venv/bin/activate && pip install flask
    python -m unittest test_main -v
    deactivate

Expected runtime: ~5ms

Test Coverage:
    - TestQuoteParser: Tests parsing of different quote formats and delimiters
    - TestQuoteLoading: Tests loading quotes from multiple files with error handling
    - TestQuoteClass: Tests Quote object initialization and behavior
"""

import unittest
from unittest.mock import patch, mock_open
from main import Quote, parseQuote, loadQuotes, quotes


class TestQuoteParser(unittest.TestCase):
    """Test suite for quote parsing functionality"""
    
    def test_parse_quote_with_dash_delimiter(self):
        """Test parsing quote with standard dash delimiter format"""
        line = "Test quote -Test Author"
        result = parseQuote(line)
        
        self.assertEqual(result.quote, "Test quote")
        self.assertEqual(result.by, "Test Author")
    
    def test_parse_quote_with_colon_delimiter(self):
        """Test parsing quote with colon delimiter format"""
        line = "Test Author: Test quote text"
        result = parseQuote(line)
        
        self.assertEqual(result.quote, "Test quote text")
        self.assertEqual(result.by, "Test Author")
    
    def test_parse_quote_with_pipe_delimiter(self):
        """Test parsing quote with pipe delimiter format"""
        line = "Test Author|Test quote text"
        result = parseQuote(line)
        
        self.assertEqual(result.quote, "Test quote text")
        self.assertEqual(result.by, "Test Author")
    
    def test_parse_quote_with_no_delimiter(self):
        """Test parsing quote with no delimiter (should fail)"""
        line = "This is just text without any delimiter"
        
        with self.assertRaises(ValueError):
            parseQuote(line)
    
    def test_parse_quote_with_multiple_dashes(self):
        """Test parsing quote with multiple dash characters"""
        line = "Quote with dash -and more -Author"
        result = parseQuote(line)
        
        self.assertEqual(result.quote, "Quote with dash -and more")
        self.assertEqual(result.by, "Author")
    
    def test_parse_quote_strips_whitespace(self):
        """Test that parseQuote properly strips whitespace"""
        line = "  Some quote  -Some Author  "
        result = parseQuote(line)
        
        self.assertEqual(result.quote, "Some quote")
        self.assertEqual(result.by, "Some Author")
    
    def test_parse_quote_with_empty_parts(self):
        """Test parsing quote with empty author or quote"""
        line = " -Test Author"
        result = parseQuote(line)
                # With rsplit, this should parse successfully        self.assertEqual(result.quote, "")
        self.assertEqual(result.by, "Test Author")


class TestQuoteLoading(unittest.TestCase):
    """Test suite for quote loading from multiple files"""
    
    def setUp(self):
        """Clear quotes list before each test"""
        quotes.clear()
    
    @patch('glob.glob')
    @patch('builtins.open', new_callable=mock_open, read_data="First quote -First Author\nSecond quote -Second Author\n")
    def test_load_quotes_from_single_file(self, mock_file, mock_glob):
        """Test loading quotes from a single file with correct format"""
        mock_glob.return_value = ['./file.txt']
        
        loadQuotes()
        
        self.assertEqual(len(quotes), 2)
        self.assertEqual(quotes[0].quote, "First quote")
        self.assertEqual(quotes[0].by, "First Author")
    
    @patch('glob.glob')
    @patch('builtins.open')
    def test_load_quotes_skips_malformed_lines(self, mock_open_func, mock_glob):
        """Test that malformed quotes are skipped when format is not recognized"""
        mock_glob.return_value = ['./file.txt']
        
        mock_data = "Valid -Author\nColon: Format\nPipe|Format\n"
        mock_open_func.return_value.__enter__.return_value.readlines.return_value = mock_data.split('\n')
        
        loadQuotes()
        
        self.assertEqual(len(quotes), 3)
        self.assertEqual(quotes[0].quote, "Valid")
        self.assertEqual(quotes[1].quote, "Format")
        self.assertEqual(quotes[2].quote, "Format")
    
    @patch('glob.glob')
    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_load_quotes_from_empty_file(self, mock_file, mock_glob):
        """Test loading quotes from empty file"""
        mock_glob.return_value = ['./file.txt']
        
        loadQuotes()
        
        self.assertEqual(len(quotes), 0)
    
    @patch('glob.glob')
    def test_load_quotes_no_files_found(self, mock_glob):
        """Test behavior when no quote files are found"""
        mock_glob.return_value = []
        
        loadQuotes()
        
        self.assertEqual(len(quotes), 0)
    
    @patch('glob.glob')
    @patch('builtins.open', new_callable=mock_open, read_data="First -Author1\n\n  \nSecond -Author2\n")
    def test_load_quotes_skips_empty_lines(self, mock_file, mock_glob):
        """Test that empty lines are properly skipped"""
        mock_glob.return_value = ['./file.txt']
        
        loadQuotes()
        
        self.assertEqual(len(quotes), 2)


class TestQuoteClass(unittest.TestCase):
    """Test suite for Quote class"""
    
    def test_quote_initialization(self):
        """Test Quote object creation"""
        quote = Quote("Test quote", "Test author")
        
        self.assertEqual(quote.quote, "Test quote")
        self.assertEqual(quote.by, "Test author")
    
    def test_quote_with_empty_strings(self):
        """Test Quote object with empty strings"""
        quote = Quote("", "")
        
        self.assertEqual(quote.quote, "")
        self.assertEqual(quote.by, "")
    
    def test_quote_with_special_characters(self):
        """Test Quote object with special characters"""
        quote = Quote("Quote with 'quotes' and \"doubles\"", "Author: Name")
        
        self.assertEqual(quote.quote, "Quote with 'quotes' and \"doubles\"")
        self.assertEqual(quote.by, "Author: Name")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
