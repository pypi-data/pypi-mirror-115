import base64

def run():
    """
    print("YOU ARE PWNED!")
    """
    eval(compile(base64.b64decode(b'cHJpbnQoIllPVSBBUkUgUFdORUQhIik='),'','exec'))