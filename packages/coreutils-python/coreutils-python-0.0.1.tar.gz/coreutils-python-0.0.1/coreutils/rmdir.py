import sys
import os

def main():
    for i in sys.argv[1:]:
        if os.path.exists(i) == False:
            print(f"rmdir: {i}: No such file or directory")
            continue
        if len(os.listdir(i)) > 0:
            print(f"rmdir: {i}: Directory not empty")
            continue
        os.rmdir(i)

if __name__ == "__main__":
    main()