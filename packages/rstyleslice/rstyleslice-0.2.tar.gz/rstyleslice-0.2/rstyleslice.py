from pathlib import Path as libpath


def rslice(filenames:list):
    suffixs = {}
    for x in filenames:
        suffix = libpath(x).suffix
        suffixs.setdefault(suffix, []).append(x)
    return suffixs


if __name__ == '__main__':
    files = [
        '123.txt', '456.mp4', '789.mp4', 'abc.txt', 'deg.py', 'hij.py'
    ]

    print(rslice(files))
