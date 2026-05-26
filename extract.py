import base64
import re

for name in ["light", "dark"]:
    with open(f"final-icon-{name}.svg") as f:
        svg = f.read()

    match = re.search(r'data:image/png;base64,([^"\' ]+)', svg)
    if match:
        b64 = match.group(1)
        with open(f"logo_{name}.png", "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"Extracted logo_{name}.png")
    else:
        print(f"Could not find base64 PNG in final-icon-{name}.svg")
