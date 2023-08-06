# from pdf2word import pdf2word
# from pptx2word import pptx2word
# from __init__ import __version__

from p2w4n.pdf2word import pdf2word
from p2w4n.pptx2word import pptx2word
from p2w4n import __version__

import getopt, sys
import os
def list_files_recursive():
    base = os.getcwd()
    # print(f'base={base}')
    for root, ds, fs in os.walk(base):
        for f in fs:
            suffix = os.path.splitext(f)[-1]
            # print(suffix)
            if suffix.lower() in ['.ppt', '.pptx', '.pdf']:
                
            # if f.endswith('.ppt') or f.endswith('.pptx') or f.endswith('.pdf'):
                # yield f
                fullname = os.path.join(root, f)
                # print(fullname)
                yield fullname
    # return []
def convert(f, max_pages, keep_images=False):
    suffix = os.path.splitext(f)[-1]
            # print(suffix)
    if suffix.lower() in ['.ppt', '.pptx']:
        pptx2word(f, max_pages)
    elif suffix.lower() in ['.pdf']:
        pdf2word(f, max_pages)
                
def list_files():
    base = os.getcwd()
    fs = [f for f in os.listdir(base)]
    for f in fs:
            suffix = os.path.splitext(f)[-1]
            # print(suffix)
            if suffix.lower() in ['.ppt', '.pptx', '.pdf']:
                
            # if f.endswith('.ppt') or f.endswith('.pptx') or f.endswith('.pdf'):
                yield f
                # fullname = os.path.join(root, f)
                # print(fullname)
                # yield fullname


def main():
    # 如果没有输入文件名或任何参数，就遍历当前目录，列出所有的以.ppt(x)或.pdf后缀的文件
    # 询问是否转换全部？
    # 如果不是转换全部文件，依次询问是否转换每个以.ppt(x)或.pdf后缀的文件
    # 最后问是否保留中间的jpg文件？

    print(f'p2w4n PPT/PDF转Word文档（为导入Notion）工具 - 版本 {__version__}')
    argumentList=sys.argv[1:]
    # Options
    options = "khc:p:"
    
    # Long options
    long_options = ["keep-image", "help", "convert=","pages=" ]
    
    try:
        # simulation_path = None
        # class_xlsx = None
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # checking each argument
        file_list = []
        source_file = None
        max_pages = 20
        keep_images = False

        for currentArgument, currentValue in arguments:
            print(f'currentArgument:{currentArgument}=[{currentValue}]')
            if currentArgument in ("-h", "--help"):
                print("\np2w4n是一个将PPT或PDF文件，转换为word文件，以便于导入(import)到Notion中的简单小工具")
                print ("\np2w4n [-k|--keep-image] [-p|--pages <max-pages-per-word-doc>]  [-c|--convert <pdf或ppt文件名>] ")
                print("\n可以通过 -c 或 --converrt 转换一个指定的文件。")
                print("\n如果没有指定文件，将列举当前目录中的所有.ppt/pptx, .pdf文件进行选择")
                print("\n通过 -p 或 --pages 参数来决定每个word文件导出的ppt/pdf的页面数量，控制word文件大小，Notion对此导入word文件的大小有一个限制")

                return
                
            elif currentArgument in ("-c", "--convert"):
                print ("转换文件: %s" % (currentValue))
                source_file = currentValue
            elif currentArgument in ("-k", "--keep-images"):
                print ("保留中间图片文件")
                keep_images = True
                
            elif currentArgument in ("-p", "--pages"):
                print (("每个word文件最大页面数： %s") % (currentValue))
                try:
                    max_pages = int(currentValue)
                except Exception as e:
                    max_pages = 20
                
        if source_file is None:
            # 遍历当前目录，列出所有的以.ppt(x)或.pdf后缀的文件
            print('目录下全部PPT或PDF文件：')
            file_list = list_files()
        else:
            # file_list.append(source_file)
            convert(source_file, max_pages, keep_images)
            return
        # print(f'Files: {file_list}')
        index = 1
        convert_list = []
        for f in file_list:
            print(f'{index}.\t{f}')
            index += 1
            convert_list.append(f)
        action = input(f'[A] (全部转换)\n[S] (让我选择)\n您的选择是:')
        todo = 0
        if action.lower() == 'a' or action.lower() == 'all':
            todo = 1
        elif action.lower() == 's' or action.lower() == 'select':
            todo = 2

        if todo == 0:
            print("您没有选择任何文件转换，退出。")
            return
        for file in convert_list:
            if todo == 1:
                convert(file, max_pages, keep_images)
            else:
                to_convert = input(f'转换 [{file}] ? [Y/N] ')
                if to_convert.lower() == 'y' or to_convert.lower() == 'yes':
                    convert(file, max_pages, keep_images)

    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

if __name__ == "__main__":
    print(f'\n{sys.argv[0]}')
    main()