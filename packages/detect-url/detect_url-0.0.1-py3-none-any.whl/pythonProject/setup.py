from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Phishing Detector'

# this grabs the requirements from requirements.txt
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
# fastapi==0.87.0
# importlib-metadata==5.0.0
# Jinja2==3.1.2
# pymongo==4.3.2
# pydantic==1.10.2
# starlette==0.21.0
# tldextract==3.4.0
# tqdm==4.64.1
# typing-extensions==4.4.0
# urllib3==1.26.12
# uvicorn==0.19.0

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="phishingurldetector",
    version=VERSION,
    author="Lionel Messi",
    author_email="donotcontact@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,

    keywords=['python', 'detecturl'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
