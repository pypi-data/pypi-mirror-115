import os


def mkdir(name):
    os.makedirs(name)


def writepy(file, contents):
    if not os.path.exists(file):
        with open(file, "w+") as f:
            f.write(contents)
