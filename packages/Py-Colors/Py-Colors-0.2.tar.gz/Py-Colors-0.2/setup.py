import setuptools
with open("README.md", 'r', encoding='utf-8') as file:
    long_description = file.read()
setuptools.setup(
    name='Py-Colors',
    version='0.2',
    description='Library For Coloring And Formatting Terminal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/pmk456/Py-Colors",
    author="Patan Musthakheem",
    author_email="patanmusthakheem786@gmail.com",
    license="Apache 2.0",
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    project_urls={
        'Documentation': 'https://github.com/pmk456/Py-Colors',
        'Source': 'https://github.com/pmk456/Py-Colors',
        'Tracker': 'https://github.com/pmk456/Py-Colors/issues'
    },
    python_requires=">=3.5",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
