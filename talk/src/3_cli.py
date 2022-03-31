import sys


def greet(name):
    print("hoi zaeme, hoi", name)


def main():
    args = sys.argv[1:]
    greet(args)


if __name__ == "__main__":
    main()
