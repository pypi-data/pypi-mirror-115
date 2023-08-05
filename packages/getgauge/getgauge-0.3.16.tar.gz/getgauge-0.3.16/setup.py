from distutils.core import setup

setup(
    name='getgauge',
    packages=['getgauge', 'getgauge/messages'],
    version='0.3.16',
    description='Enables Python support for Gauge',
    author='Gauge Team',
    author_email='getgauge@outlook.com',
    url='https://github.com/getgauge/gauge-python',
    download_url='https://github.com/getgauge/gauge-python/archive/v0.3.16.zip',
    keywords=['testing', 'gauge', 'gauge-python', 'getgauge', 'automation'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=['redBaron', 'debugpy', 'grpcio==1.34.0', 'protobuf>=3.5.2'],
    extras_require={
		':python_version == "2.7"': ['futures']
	},
)
