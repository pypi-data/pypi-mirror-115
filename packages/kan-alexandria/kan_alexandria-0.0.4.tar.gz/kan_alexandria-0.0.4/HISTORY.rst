.. changelog:

Release History
===============

0.0.3 - 2021-08-10
-----
Based on the previous version by Sang Han, this fork version has 
been modified to output more data from Google Books API and return the data
in a more useful format (Python Dict).

The resulting dict has the following keys:
- title
- author
- isbn
- categories
- description
- img #url to the cover image
- publisher
- publishedDate #YYYY-MM-DD
- pageCount

To access the dict, import the module as following:
from kan.book_api import search_book_kan

Then use the function search_book_kan() to get the data.
Use: search_book_kan(title, author)

When the Google Books API does not return any result, the function will return
the dict with the empty keys holding 'N/A' values.

0.0.2
-----
- Bug fixes and speed improvements. More compact interface
- Book models update
- Completed Backend API for Google Books
- Added verbose flag

0.0.1
-----
- Bug Fixes
- Improved loadtime by applying fieldstring parameter at url creation.
- Added Subparser
- Allow search using ISBN

0.0.0
------
- Initial registration and release on pypi
- Built command line parser
- Basic Client Interface and Implementation for Google Books
- Added support for optional search arguments
