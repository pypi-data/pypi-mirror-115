import sys
import os

def main():
    if len(sys.argv) < 2:
        sys.argv.append(".")
    for i in sys.argv[1:]:
        if os.path.exists(i) == False:
            print(f"ls: {i}: No such file or directory")
            continue
        if os.path.isfile(i) == True:
            print(i)
            continue
        lis = os.listdir(i)
        if len(sys.argv[1:]) > 1:
            print(i + ":")
        for j in lis:
            print(j)
        if len(sys.argv[1:]) > 1:
            print("\n")

if __name__ == "__main__":
    main()