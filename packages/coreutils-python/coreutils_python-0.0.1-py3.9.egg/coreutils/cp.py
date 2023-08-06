import sys
import os
import shutil

def main():
    if os.path.isdir(sys.argv[-1]) == False and len(sys.argv[1:-1]) > 1:
        print(f"cp: {sys.argv[-1]} is not a directory")
        exit()
    for i in sys.argv[1:-1]:
        shutil.copy(i, sys.argv[-1])

if __name__ == "__main__":
    main()