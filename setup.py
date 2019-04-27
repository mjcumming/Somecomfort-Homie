import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='Somecomfort Homie 3',
      version='0.0.4',
      description='Homie 3 for Honeywell Total Comfort North America',
      author='Michael Cumming',
      author_email='mike@4831.com',
      long_description=long_description,
      long_description_content_type="text/markdown",      
      url='https://github.com/mjcumming/Homie',
      keywords = ['HOMIE','MQTT','Somecomfort','Honeywell'],  
      packages=setuptools.find_packages(exclude=("test.py",)),
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],      
    install_requires=[
        'Homie3',
        'somecomfort',
        'pyyaml',
        'timer3'
    ]      
)
