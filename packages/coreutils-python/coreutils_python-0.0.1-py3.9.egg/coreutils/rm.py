import sys
import os

def rmdir(dirname):
    lis = os.listdir(dirname)
    for i in lis:
        if os.path.isfile(os.path.join(dirname, i)) == True:
            os.remove(os.path.join(dirname, i))
        elif len(os.listdir(os.path.join(dirname, i))) == 0:
            """空文件夹"""
            os.rmdir(os.path.join(dirname, i))
        else:
            rmdir(os.path.join(dirname, i))
    os.rmdir(dirname)

def main():
    for i in sys.argv[1:]:
        if i[0] == "-":
            continue
        if os.path.exists(i) == False:
            print(f"rm: {i}: No such file or directory")
            continue
        if os.path.isdir(i) == True:
            if ("-r" in sys.argv[1:]) == False:
                print(f"rm: {i}: is a directory")
                continue
            else:
                rmdir(i)
                continue
        os.remove(i)

if __name__ == "__main__":
    main()