# DISCLAIMER
This repository is not at all associated with brainyquote.com . The software is only to be used for educational purposes only. By downloading this code you agree with this disclaimer and any misuse is not held in responsibility with the author.
## brainyquote-api
**UNOFFICIAL** API for [brainyquotes.com](brainyquotes.com) . Must have >= Python 3.7 installed for this program to function properly.
## Installation

```
pip install brainyquote-api
```

## Usage

```python
from brainyquote_api import quote

# Example of this module in use.

# This is a tool used to scrape the brainyquote.com page for quotes based on the specified category 
# It returns a randomised quote based on the maximum page you want the scraping tool to go through
# An example of this tool in action would be this
quote = quoteCall(category()[79], 3) # This would return the randomised quote from the specified category given by category()[79]

# This function returns a list of all categories on the website and when you call the quoteCall and use category()[*index value*] then it uses the specified category according to its index value in the list
categories = category()

```


