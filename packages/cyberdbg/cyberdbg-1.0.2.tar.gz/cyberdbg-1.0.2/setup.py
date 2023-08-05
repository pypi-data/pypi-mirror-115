from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'Sample Package made for a demo \
	of its making for the GeeksforGeeks Article.'

setup(
		name ='cyberdbg',
		version ='1.0.2',
		author ='chopstickxs',
		author_email ='chopstickxs@yandex.com',
		url ='https://github.com/chopstickxs/Cyberdbg',
		description ='Demo Package for GfG Article.',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'cyberdgb = cyberdbg.gfg:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='dbg cyber',
		install_requires = requirements,
		zip_safe = False
)
