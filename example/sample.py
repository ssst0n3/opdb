def f():
    a, b = 1, 0
    if a or b:
        return a


def main():
    res = f()
    print(res)


if __name__ == '__main__':
    main()
