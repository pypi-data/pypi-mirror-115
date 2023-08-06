import sys
import os

def main():
    if os.path.isdir(sys.argv[-1]) == False and len(sys.argv[1:-1]) > 1:
        print(f"mv: {sys.argv[-1]} is not a directory")
        exit()
    for i in sys.argv[1:-1]:
        if os.path.isfile(sys.argv[-1]):
            os.remove(sys.argv[-1])
            os.rename(i, sys.argv[-1])
        else:
            os.rename(i, sys.argv[-1])

if __name__ == "__main__":
    main()