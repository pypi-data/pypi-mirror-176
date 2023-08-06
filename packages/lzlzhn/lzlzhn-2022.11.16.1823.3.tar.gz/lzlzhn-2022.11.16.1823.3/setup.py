from setuptools import setup, find_packages

setup(
    name='lzlzhn',
    version='2022.11.16.1823.3',
    description="一个很会玩的第三方库,更新版本号与更新/修复个数有关",
    long_description='HELLO! 感谢你下载我的第三方库！十分感谢！官网：http://zlteam.top 注册登录后点击lzlzhn第三方库按钮即可',
    include_package_data=True,
    author='梦醒孤漠吃饺子',
    author_email='liuniandexiaohuo@qq.com',
    license='MIT License',
    url='http://zlteam.top',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=['pyperclip', 'PyAutoGUI', 'pygame', 'qrcode', 'MyQR', 'PyQt5', 'PyQt5-stubs'],

)
