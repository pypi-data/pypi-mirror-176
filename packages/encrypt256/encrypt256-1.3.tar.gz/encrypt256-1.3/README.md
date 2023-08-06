# 字符串|字节串|文件 加密器

# 项目介绍

    ● 一个字符串|字节串|文件 加密器

    ● 此包是对pycryptodome进行二次封装
    ● 底层加密算法为AES-CBC-256
    ● 加密时, 会自动设置创建随机salt和随机iv, 并生成原始明文的校验值
    ● 解密时, 会自动校验"解密得到的明文"与"初始明文是否一致"

# 作者资料

    昵称: jutooy

    邮箱: jutooy@qq.com

    技术支持: jutooy@qq.com
    注：
        1、此为人道主义免费支持，考虑到数据无价才开通！
        若加密遇到问题请自行学习，仅当解密重要文件失败时才联系我。

        2、本项目代码逻辑严谨，并经过严格测试，代码没有问题。

    技术博客(欢迎来踩): https://www.yuque.com/jutooy/code

# 语法

## 导入

    from encrypt256 import Encrypt256
    from random import randbytes, choice, randint
    from pathlib import Path as libpath


## 加密 字符串|字节串

    plaText = choice([
        '黄河之水天上来',  # 可以加密字符串
        randbytes(10000)  # 可以加密字节串
    ])

    password = choice([
        '床前明月光',  # 密钥可以是字符串
        randbytes(10000),  # 密钥可以是字节串
        71395003615  # 密钥可以是整数
    ])

    checkSize = randint(0, 255)  # 解密时校验指纹长度，可为0

    # 加密
    cipText = Encrypt256(password=password).encrypt(
        text = plaText,
        checkSize = checkSize
    )

    # 解密
    NewPlaText = Encrypt256(password=password).decrypt(text=cipText)

    assert plaText != cipText
    assert plaText == NewPlaText


## 加密文件

    plaFile = "C:\下载\原文件.temp"
    cipFile = "C:\下载\加密文件.temp"  # 此时不存在
    NewPlaFile = "C:\下载\解密文件.temp"  # 此时不存在

    password = choice(['床前明月光', randbytes(10000), 71395003615])
    checkSize = randint(0, 255)

    # 加密
    Encrypt256(password=password).encryptFile(
        fpath = plaFile,  # 原文件路径
        outpath = cipFile,  # 加密文件输出路径
        checkSize = checkSize  # 校验值长度
    )

    # 解密
    Encrypt256(password=password).decryptFile(
        fpath = cipFile,  # 加密文件路径
        outpath = NewPlaFile  # 解密文件输出路径
    )

    def readFile(fpath):
        return libpath(fpath).read_bytes()
    
    assert readFile(plaFile) != readFile(cipFile)
    assert readFile(plaFile) == readFile(NewPlaFile)
