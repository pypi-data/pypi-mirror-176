from setuptools import setup, find_packages

setup(
    name='PyOSCmd',  # 包名
    version='0.1',  # 版本
    description="PySysCmd是一个用于开发终端PY命令行的第三方库，简单，易用。",  # 包简介
    long_description=open('.\README.md', 'r', encoding="utf-8").read(),  # 读取文件中介绍包的详细内容
    long_description_content_type="text/markdown",
    include_package_data=True,  # 是否允许上传资源文件
    author='PYmili',  # 作者
    author_email='mc2005wj@163.com',  # 作者邮件
    maintainer='PYmili',  # 维护者
    maintainer_email='mc2005wj@163.com',  # 维护者邮件
    license='MIT License',  # 协议
    url='https://github.com/PYmili',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    python_requires='>=3.8',  # 设置python版本要求
    install_requires=[''],  # 安装所需要的库
    # entry_points={
    #     'console_scripts': [
    #         ''],
    # },  # 设置命令行工具(可不使用就可以注释掉)

)