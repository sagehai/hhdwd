import re
from bs4 import BeautifulSoup
import xlwt
import sys
import os

renumber = re.compile(r'<strong>(.*?)</strong>')
resubject = re.compile(r'</strong> (.*?)<input id="question')
reanswer = re.compile(r'<input id="answer\d*" type="hidden" value="(.*?)"/>')
savepath = os.getcwd()
args = sys.argv

def main():
    savepath = os.getcwd() + "/答案.xls"
    if len(args) != 1:
        file = open(args[1], "rb")

    if sys.platform == "linux":
        gavepash = os.getcwd() + "/"
    else:
        gavepash = os.getcwd() + "\\"

    test = [f for f in os.listdir(os.getcwd()) if '.html' in f]
    if len(test) == 1:
        file = open(gavepash + test[0],"rb")
    else:
        if len(test) == 0:
            print("未在当前目录下找到保存的网页")
            file = ""
            input("按回车键键退出")
            exit()
        else:
            print("请选择你要分析的网页")
        for i in test:
            print(i)
            a = int(input("请输入数字:")) - 1
            file = open(gavepash + test[a],"rb")

    html = file.read()
    bs = BeautifulSoup(html, "html.parser")
    table = bs.find_all("table", align="center")
    datalist = []
    for item in table[1].find_all("td", colspan="4"):
        data = []
        item = str(item)
        number = re.findall(renumber, item)
        subject = re.findall(resubject, item)
        answer = re.findall(reanswer, item)

        if number:
            data.append(number)
            data.append(subject)
            data.append(answer)

        if data:
            datalist.append(data)

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('答案', cell_overwrite_ok=True)
    for i in range(0, len(datalist)):
        data = datalist[i]
        for j in range(0, 3):
            sheet.write(i, j, data[j])

    book.save(savepath)



if __name__ == '__main__':
    main()
