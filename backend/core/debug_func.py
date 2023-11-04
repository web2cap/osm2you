from colorama import Back, Style


def aprint(data):
    print(Back.GREEN)
    print("*" * 20)
    print(Style.RESET_ALL)
    print(data)
    print("-" * 20)
