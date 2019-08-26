import os
def ListFilesToTxt(dir, file, wildcard, recursion):
    exts = wildcard.split(" ")
    files = os.listdir(dir)
    for name in files:
        #print(name)
        fullname = os.path.join(dir, name)  ##吧目录和文件名生成一个目录
        if (os.path.isdir(fullname) & recursion):  #判断路径是否为文件夹
            ListFilesToTxt(fullname, file, wildcard, recursion)
        else:
            for ext in exts:
                if (name.endswith(ext)):
                    file.write(name + "\n")
                    break


def Test():
    dir = "../爬取起点小说_语音识别/凡人修仙之仙界篇"
    outfile = "../爬取起点小说_语音识别/凡人修仙之仙界篇/A目录.txt"
    wildcard = ".txt .exe .dll .lib"

    file = open(outfile, "w")
    if not file:
        print("cannot open the file %s for writing" % outfile)
    ListFilesToTxt(dir, file, wildcard, 1)
    file.close()


Test()
