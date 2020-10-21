import re

data = \
["definitions/inline_response_200", \
"""
description: Default OK
schema:
  type: object
  properties:
    data:
      type: string
      example: OK
""", \
"definitions/inline_response_error", \
"""
description: Default error
schema:
  type: object
  properties:
    error:
      $ref: '#/definitions/Error'
"""]

def find_match(line):
    for p, r in zip(data[::2], data[1::2]):
        if p in line:
            return r
    return None

with open('swagger.yaml') as original:
    with open('swagger-new.yaml', 'wt') as modified:
        for line in original:            
            replacement = find_match(line)
            if replacement:
                m = re.search(r"\S", line)
                indent = line[:m.start()]
                msg = replacement.replace("\n", "\n"+indent).strip()
                modified.write(indent + msg + "\n")
            else:
                modified.write(line)
                replaced = False
