# common.py

def echo(some_text):
    print(some_text)

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False