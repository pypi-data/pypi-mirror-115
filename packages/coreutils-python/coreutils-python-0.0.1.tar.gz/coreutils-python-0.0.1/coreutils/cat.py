import sys
import os

def main():
    for i in sys.argv[1:]:
        if os.path.exists(i) == False:
            print(f"cat: {i}: No such file or directory")
            continue
        if os.path.isdir(i) == True:
            print(f"cat: {i}: Is a directory")
            continue
        with open(i, "rb") as f:
            for byte in f.read():
                print(chr(byte), end = "")

if __name__ == "__main__":
    main()