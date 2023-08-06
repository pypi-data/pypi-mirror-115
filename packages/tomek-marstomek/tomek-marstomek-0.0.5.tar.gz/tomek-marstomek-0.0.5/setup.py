# https://packaging.python.org/tutorials/packaging-projects/
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='tomek-marstomek',
      version='0.0.5',
      description='My CFFI python example hash table',
      long_description=long_description,
      author='Tomasz Marszalek',
      author_email='marstomek@gmail.com',
      url='http://mt-software.info/',
      package_dir={"": "."},
      package_data= {'':['libperson.so', '_person.cpython-39-x86_64-linux-gnu.so']},
      packages=['tomek'], # can use : packages=setuptools.find_packages(where="."),
      options={"bdist_wheel": {"universal": False}},
	install_requires=[],
	setup_requires=["pytest"],
      python_requires=">=3.6",
      platforms=['linux'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
     )
