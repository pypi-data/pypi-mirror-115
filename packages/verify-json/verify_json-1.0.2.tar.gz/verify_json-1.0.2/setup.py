import requests
from setuptools import setup, find_packages
def md_to_rst(from_file, to_file):
    """
    将markdown格式转换为rst格式
    @param from_file: {str} markdown文件的路径
    @param to_file: {str} rst文件的路径
    """
    # response = requests.post(
    #     url='http://c.docverter.com/convert',
    #     data={'to': 'rst', 'from': 'markdown'},
    #     files={'input_files[]': open(from_file, 'rb')}
    # )
    #
    # if response.ok:
    #     with open(to_file, "wb") as f:
    #         f.write(response.content)


# if __name__ == '__main__':
    # md_to_rst("README.md", "README.rst")

setup(
    name="verify_json",
    version="1.0.2",
    packages=find_packages(),
    description='A JSON contract tool that outputs build matches',
    author="Ze Hua",
    author_email = '1737985326@qq.com',
    url='https://github.com/DaoSen-v/JsonDiff',
    license='MIT',
    zip_safe = False,
    install_requires = [
    ],
    long_description=open("README.rst", encoding='utf-8').read(),
    entry_points={
    },
    data_files=["README.rst"]
)