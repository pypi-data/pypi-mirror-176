import setuptools
with open(r'README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='pyEasyWeb3',
	version='1.0.4.2',
	author='Fitrad3w',
	author_email='onigirisell@protonmail.com',
	description='library for easy web3 usage (default network BSC)',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/onigirisell/pyEasyWeb3',
	packages=['pyEasyWeb3', 'pyEasyWeb3/data', 'pyEasyWeb3/metamask'],
	install_requires= ['openpyxl==3.0.10', 'XlsxWriter==3.0.3', 'asyncio==3.4.3', 'eth-account==0.5.9', 'web3==5.31.1'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.9',
)