import re

regex = re.compile('[^a-zA-Z0-9-]')
#First parameter is the replacement, second parameter is your input string
x = regex.sub('', 'h3llo w0rld!!#]$')

print(x)