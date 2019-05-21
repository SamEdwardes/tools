'''
TITLE: outlook emails to list
DESCRIPTION: takes text from clipboard (emails/names copied from outlook) and returns a list to clipboard)
---
AUTHOR: Sam Edwardes
DATE: 2019-05-12
NOTES: n/a
'''

import pyperclip

# get test from clipboard
emails = pyperclip.paste()

# clean text
emails_list = emails.replace("; ", "\n").replace(" <", " - ").replace(">", "")

# return value to clipboard
pyperclip.copy(emails_list)

