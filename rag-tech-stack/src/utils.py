

def load_text(fname):
    if fname is None:
        raise ValueError("fname is None")
    with open(fname, "r") as f:
        return f.read()

def load_prompt(fname):
    if fname is None:
        raise ValueError("fname is None")
    with open(fname, "r") as f:
        return f.read()