# Ancient Book Search

ABS(Ancient Book Search) is an interface for searching ancient books located in my college. It is based on ElasticSearch to index meta data and basic informations and create a simple web site with supports of Flask.

## The data.txt

The data in `data.txt` is collected from my college's library. They were writen in some doc or pdf files which is not convenient to search the book needed. With help of some packages in Python (win32com, pdfminer, etc), I exported the content into a plain text file. Although the text is ready, the structure of text is still in a mess. That's why I wrote the script `parse.py`, which helps to read and parse the meta data such as title, authors, abstract, publish time, etc, and import these meta data into ElasticSearch.

## Dependency

- ElasticSearch
- Flask
- Gunicorn(optional)

## Install and startup

First, the data of ancient books must be imported and indexed into ElasticSearch engine by using `parse.py`.

    python parse.py

After running the script above, the meta data in `data.txt` will be read and saved in ElasticSearch. Then, just start the web site.

    python server.py

or using Gunicorn:

    gunicorn -w 2 -b 0.0.0.0:60423 server:app

and using `Nginx` or `Apache` to do reverse proxy.
