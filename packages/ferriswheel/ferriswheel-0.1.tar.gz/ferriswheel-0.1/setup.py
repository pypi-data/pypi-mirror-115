import setuptools

setuptools.setup(name='ferriswheel',
      version='0.1',
      description='https://ferris.chat API library',
      url='http://github.com/randomairborne/ferriswheel',
      author='valkyrie_pilot',
      author_email='valk@randomairborne.dev',
      license='LGPL',
      install_requires=[
          'emoji',
      ],
      project_urls={
        "Bug Tracker": "https://github.com/randomairborne/ferriswheel",
      },
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      python_requires=">=3.6",)
