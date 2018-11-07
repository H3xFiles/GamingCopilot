import psutil

FILENAME = "autokeyboard.py"
isTheProcessOn = False


def isRunning(name):
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == name:
            return True
        else:
            return False


def execfile(status, filepath, globals=None, locals=None):
    if not status:
        if globals is None:
            globals = {}
        globals.update({
            "__file__": filepath,
            "__name__": "__main",
        })
        with open(filepath, 'rb') as file:
            exec(compile(file.read(), FILENAME, 'exec'), globals, locals)
            return True
    else:
        return True


print("AutoUpUp is on.")
while True:
    if isTheProcessOn:
        continue
    else:
        isTheProcessOn = execfile(isTheProcessOn, FILENAME)
