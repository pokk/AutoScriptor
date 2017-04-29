""" Created by jieyi on 4/28/17. """
import io
import sys

# Simulate the redirect stdin.
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inp = ''.join(open(filename, "r").readlines())
    sys.stdin = io.StringIO(inp)


def main():
    print('hello world!!!')


if __name__ == '__main__':
    main()
