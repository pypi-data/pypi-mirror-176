# 项目介绍

    ● 一个 字符串|字节串|文件 加密器

    ● 此包是对pycryptodome进行二次封装

    ● 底层加密算法为AES-CBC-256

    ● 加密时, 会自动设置创建随机salt和随机iv, 并生成原始明文的校验值

    ● 解密时, 会自动校验"解密得到的明文"与"初始明文是否一致"

# 作者资料

昵称: jutooy

邮箱: jutooy@qq.com

# 语法

    from encrypt256 import Encrypt
    from random import randbytes, choice, randint
    from os.path import abspath
    from pathlib import Path as libpath


    # 加密 字符串|字节串

    plaText = choice(['黄河之水天上来', randbytes(10000)])
    password = choice(['床前明月光', randbytes(10000), 71395003615])
    checkSize = randint(0, 255)

    cipText = Encrypt(password=password).encrypt(text=plaText, checkSize=checkSize)
    NewPlaText = Encrypt(password=password).decrypt(text=cipText)

    assert plaText != cipText
    assert plaText == NewPlaText


    # 加密文件

    baseDir = abspath(libpath(__file__).parent)
    plaFile = f"{baseDir}/plaFile.temp"
    cipFile = f"{baseDir}/cipFile.temp"
    NewPlaFile = f"{baseDir}/NewPlaFile.temp"

    plaText = randbytes(10000)
    password = choice(['床前明月光', randbytes(10000), 71395003615])
    checkSize = randint(0, 255)

    libpath(plaFile).write_bytes(plaText)
    Encrypt(password=password).encryptFile(fpath=plaFile, outpath=cipFile, checkSize=checkSize)
    Encrypt(password=password).decryptFile(fpath=cipFile, outpath=NewPlaFile)

    assert plaText != libpath(cipFile).read_bytes()
    assert plaText == libpath(NewPlaFile).read_bytes()

    libpath(plaFile).unlink(missing_ok=True)
    libpath(cipFile).unlink(missing_ok=True)
    libpath(NewPlaFile).unlink(missing_ok=True)
