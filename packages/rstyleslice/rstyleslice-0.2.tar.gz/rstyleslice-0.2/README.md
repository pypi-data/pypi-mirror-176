# 项目介绍

根据文件后缀分类文件

# 作者资料

昵称: jutooy

邮箱: jutooy@qq.com

# 使用方法

    from rstyleslice import rslice

    files = [
        '123.txt', '456.mp4', '789.mp4', 'abc.txt', 'deg.py', 'hij.py'
    ]

    print(rslice(files))

    >>> {'.txt': ['123.txt', 'abc.txt'], '.mp4': ['456.mp4', '789.mp4'], '.py': ['deg.py', 'hij.py']}