from setuptools import setup, find_packages
import testinlabel

filepath = 'README.rst'

setup(
    name="testinlabel",
    version=testinlabel.VERSION,
    keywords=["云测", "数据集","yuncedata", "testin", "testinlabel"],
    description="云测数据 标注平台pythonSDK",
    long_description=open(filepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url = "http://ai.testin.cn/",
    author = "hide-in-code",
    author_email = "hejinlong@testin.cn",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tla = testinlabel.cli.run:main'
        ]
    },
    include_package_data=True,
    platforms="any",
    install_requires=[
        "requests",
        "click",
    ],
    data_files=[filepath],
)
