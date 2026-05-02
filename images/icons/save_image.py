import base64, sys

b64_data = sys.argv[1]
with open(sys.argv[2], 'wb') as f:
    f.write(base64.b64decode(b64_data))
