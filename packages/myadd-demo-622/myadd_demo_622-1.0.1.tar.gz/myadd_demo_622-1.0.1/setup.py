import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myadd_demo_622",  # 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    version="1.0.1",  # 程序版本
    author="XDD",  # 项目作者
    author_email="xdd2026@qq.com",  # 作者邮件
    description="我的测试案例",  # 项目的一句话描述
    long_description=long_description,  # 加长版描述
    long_description_content_type="text/markdown",  # 描述使用Markdown
    url="https://github.com/xdd1997/pypi_demo_xdd.git",  # 项目地址
    packages=setuptools.find_packages(),  # 无需修改
    classifiers=[
        "Programming Language :: Python :: 3",  # 使用Python3
        "License :: OSI Approved :: Apache Software License",  # 开源协议
        "Operating System :: OS Independent",
    ],
)