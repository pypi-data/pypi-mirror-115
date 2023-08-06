version='0.0.1.4' # change this to change the version
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='ferriswheel',
      version=version,
      description='https://ferris.chat API library',
      url='http://github.com/randomairborne/ferriswheel',
      author='valkyrie_pilot',
      author_email='valk@randomairborne.dev',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='LGPL',
      install_requires=[
          'aiohttp[speedups]',
      ],
      project_urls={
        "Bug Tracker": "https://github.com/randomairborne/ferriswheel/issues",
      },
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      python_requires=">=3.6",)
