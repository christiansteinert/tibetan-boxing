## Tibetan grammar boxing tool
This little application allows to mark up the grammar structure of Tibetan sentences by defining boxes around various parts of speech and labeling these boxes. 

You can type a relatively simple text format on the left side of the screen and the right side of the screen will show a generated PDF document that is based on your input. 

You can see the application in action at https://tibetanboxing.christian-steinert.de

## Dependencies
The implementation is done in Python by using the Flask framework to run as a web application.

Besides Python and Flask the application uses some external programs and fonts that can be installed on Fedora with:
```
dnf install pandoc texlive-xetex jomolhari-fonts liberation-fonts
```

For deployment a webserver is needed that supports the Python WSGI (Web Server Gateway Interface). For example, Apache with mod_wsgi can be used. In that case Apache can be directed to execute the Flask application by mapping the web root of a website to the python script: `WSGIScriptAlias / /path/to/app.py`, for example `WSGIScriptAlias / /var/www/html/app.py`
