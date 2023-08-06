import setuptools

setuptools.setup(
    name="my_tourdata",
    version="0.0",
    license='MIT',
    author="jongphago",
    author_email="jonghyun.d.kim@gmail.com",
    description="test-package",
    long_description=open('README.md').read(),
    url="https://github.com/jongphago",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)