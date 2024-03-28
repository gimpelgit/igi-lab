from geometric_lib import circle, square


def main():
    try:
        with open('param.txt', 'r') as file:
            param = float(file.read())
            print(f"Parameter: {param}")
            print(f"Square area: {square.area(param)}")
            print(f"Square perimeter: {square.perimeter(param)}")
            print(f"Circle area: {circle.area(param)}")
            print(f"Circle perimeter: {circle.perimeter(param)}")
    except IOError:
        print("File read error")


if __name__ == '__main__':
    main()
