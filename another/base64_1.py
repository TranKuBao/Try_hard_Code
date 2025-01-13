import base64
import urllib.parse

encoded_string = "dXNlcg%3D%3D"

# URL decode
url_decoded_string = urllib.parse.unquote(encoded_string)

# Base64 decode
decoded_string = base64.b64decode(url_decoded_string).decode('utf-8')

print(decoded_string)
