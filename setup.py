from setuptools import setup, find_packages

setup(
    name='chatgpt_serve',
    # 指定版本号
    version='1.1.2',
    # 这是对当前项目的一个描述
    description='tomserve项目',
    # 作者是谁，指的是此项目开发的人，这里就写你自己的名字即可
    author='openai',
    # 作者的邮箱
    author_email='openai@outlook.com',
    install_requires=["Flask", "Flask-Cors", "openai", "gunicorn", "PyMySQL", "numpy"],
    packages=find_packages(),
    include_package_data=True,
)
