import sys
import os

def main():
    for i in sys.argv[1:]:
        if os.path.exists(i) == True:
            print(f"mkdir: {i}: File exists")
            continue
        os.mkdir(i)

if __name__ == "__main__":
    main()