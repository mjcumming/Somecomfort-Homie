import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='Somecomfort Homie 4',
      version='0.1.7',
      description='Homie 4 for Honeywell Total Comfort North America',
      author='Michael Cumming',
      author_email='mike@4831.com',
      long_description=long_description,
      long_description_content_type="text/markdown",      
      url='https://github.com/mjcumming/Somecomfort-Homie',
      keywords = ['HOMIE','MQTT','Somecomfort','Honeywell'],  
      packages=setuptools.find_packages(exclude=("test.py",)),
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],      
    install_requires=[
        'Homie4',
        'somecomfort',
        'pyyaml',
        'timer3'
    ],
    scripts=['somecomfort_homie_start.py'],
)
