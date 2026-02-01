from flask import Flask
from flask import jsonify
import random
import os
import glob

QUOTES_DIR = "./" # directory containing quote files
quotes = [] # stores all quotes from all sources

# a quote
class Quote(object):
    def __init__(self, quote, by):
        self.quote = quote
        self.by = by

# Parse a single quote line (assumes "-" delimiter for all formats)
def parseQuote(line):
    """Parse a quote line and return a Quote object.
    
    Currently supports format: "quote text - author"
    """
    quote, by = line.split("-")
    return Quote(quote.strip(), by.strip())

# Loads quotes from all available quote files
def loadQuotes():
    """Load quotes from multiple sources in the quotes directory."""
    quote_files = glob.glob(os.path.join(QUOTES_DIR, "quotes*.txt"))
    
    for quote_file in quote_files:
        print(f"Loading quotes from {quote_file}")
        with open(quote_file) as file:
            lines = file.readlines()
            lines = [x.strip() for x in lines if x.strip()] 
            
            for line in lines:
                try:
                    quote = parseQuote(line)
                    quotes.append(quote)
                except Exception as e:
                    # Skip malformed quotes silently
                    print(f"Warning: Failed to parse quote: {line[:50]}... Error: {e}")
                    continue
    
    print(f"Loaded {len(quotes)} quotes from {len(quote_files)} sources")
            
app = Flask(__name__)

# Gets a random quote 
@app.route("/api/quote")
def quote():
    q = random.choice(quotes) # selects a random quote from file
    return jsonify({"quote": q.quote, "by": q.by}) # return a quote

# 404 Erorr for unknown routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Resource not found"}), 404

if __name__ == '__main__':
    loadQuotes() # load quotes 
    app.run(host='0.0.0.0', port=5000, debug=True) # run application
    