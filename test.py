import sys

def input_by_server(argv):
    v = int(argv[1]) + 1
    print(v)

if __name__ == "__main__":
    input_by_server(sys.argv)
