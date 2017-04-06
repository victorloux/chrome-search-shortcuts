#!/usr/bin/env python3

"""This scripts exports user-defined keywords for Google Chrome's
custom search engines as a JSON

@todo: allow importing too

Released under the WTFPL v2 <http://www.wtfpl.net/txt/copying/>
2017 Victor Loux <https://github.com/victorloux/chrome-search-shortcuts>"""

from os.path import expanduser
import sqlite3
import json

try:
    # This expands the ~ as it would in a shell, and is cross-platform
    home = expanduser("~")

    # Load up the Chrome database called "Web Data" (no extension).
    # file:, ?mode=ro and uri=True are used for enabling read-only mode
    # to avoid any accidental disaster (doesn't prevent locks though)
    #
    # @todo: make this cross-platform (it's OSX only for now)
    db = sqlite3.connect("file:" + home + "/Library/Application Support/Google/Chrome/Default/Web Data?mode=ro", uri=True)

    # Create a cursor and run a query for all keywords that don't have dots
    # (i.e. unlikely to have been created automatically by policy)
    # It's a bit of a dumb and inaccurate filter but afaik there's
    # no actual flag in the database to differentiate user-created vs policy
    cur = db.cursor()
    cur.execute("""SELECT short_name, keyword, url
                   FROM `keywords`
                   WHERE `keyword` NOT LIKE '%.%';""")

    # Print all as a JSON!
    results = cur.fetchall()
    print(json.dumps(results))

except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
    error_message = str(e)

    if error_message == "database is locked":
        print("The database seems locked. You need to quit Chrome first!")

    elif error_message == "unable to open database file":
        print("The database file could not be found. You might be \
              on an unsupported platform.")

    else:
        print("DB error: " + error_message)

    exit(1)  # Error exit status
