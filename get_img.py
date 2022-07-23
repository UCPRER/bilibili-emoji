import re
import requests
from pathlib import Path
import argparse


def getimg(file_path, target_dir):
    htmlContent = open(file_path, 'r', encoding='utf-8').readline()

    def cutInputByStr(startStr, endStr, inputStr):
        """
        从整段字符串中，截取多个，开头和结尾格式重复的，子串
        :param startStr:起始字符串
        :param endStr:结束字符串
        :param inputStr:整段字符串
        :return:字符串组
        """
        # 查找到，所有起始字符串的结束位置
        startsStart = [each.start()
                       for each in re.finditer(startStr, inputStr)]
        endsStart = [start + len(startStr) - 1 for start in startsStart]
        # 查找到，所有结束字符串的结束位置
        startsEnd = [each.start() for each in re.finditer(endStr, inputStr)]
        endsEnd = [start + len(endStr) - 1 for start in startsEnd]
        result = []
        for startPos, endPos in zip(endsStart, endsEnd):
            result.append(inputStr[startPos:endPos + 1 - len(endStr)])
        print("获取完成")
        return result

    def download(filename, url):
        with open(filename, 'wb+') as f:
            try:
                f.write(requests.get("http://" + url).content)
            except:
                print("下载失败")

    srcs = cutInputByStr("src=\"//i", "@", htmlContent)
    names = cutInputByStr("alt=\"\[", "\]", htmlContent)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    for name, src in zip(names, srcs):
        download(target_dir/(name+".png"), src)
    print("成功")

parser = argparse.ArgumentParser()
parser.add_argument("loc")
args = parser.parse_args()
getimg("img.txt", args.loc)
