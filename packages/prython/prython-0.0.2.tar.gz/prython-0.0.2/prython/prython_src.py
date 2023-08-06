import code

def pry():
    code.interact(local=dict(globals(), **locals()))