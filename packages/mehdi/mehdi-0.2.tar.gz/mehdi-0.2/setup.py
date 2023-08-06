from setuptools import setup, find_packages


metadata = dict(
    name="mehdi",  # Replace with your own username
    version="0.2",
    author="Stacrypt",
    author_email="Stacrypt@info.com",
    description="Stacrypt utility package",
    long_description="",
    long_description_content_type="text/markdown",
    url=None,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7')
setup(**metadata)

