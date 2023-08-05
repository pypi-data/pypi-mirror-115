import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ctextinct",
    version="3.0.0",
    description="Educational Cyber Security Chatbot - Working to Making Cyber Threats Extinct",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aapatrick/CT_Extinct/tree/master",
    author="Patrick Abdul-Ahad",
    author_email="aa.patrick@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["ctextinct"],
    include_package_data=True,
    install_requires=[
        "absl-py",
        "astunparse",
        "beautifulsoup4",
        "bs4",
        "cachetools",
        "certifi",
        "charset-normalizer",
        "click",
        "colorama",
        "flatbuffers",
        "gast",
        "google-auth",
        "google-auth-oauthlib",
        "google-pasta",
        "grpcio",
        "h5py",
        "idna",
        "joblib",
        "keras-nightly",
        "Keras-Preprocessing",
        "Markdown",
        "newsapi",
        "nltk",
        "numpy",
        "oauthlib",
        "opt-einsum",
        "pandas",
        "Pillow",
        "protobuf",
        "pyasn1",
        "pyasn1-modules",
        "python-dateutil",
        "pytz",
        "regex",
        "requests",
        "requests-oauthlib",
        "rsa",
        "six",
        "soupsieve",
        "tensorboard",
        "tensorboard-data-server",
        "tensorboard-plugin-wit",
        "tensorflow",
        "tensorflow-estimator",
        "termcolor",
        "tqdm",
        "typing-extensions",
        "urllib3",
        "Werkzeug",
        "wrapt",
        "twine"
    ],
    entry_points={
        "console_scripts": [
            "ctextinct=ctextinct.__main__:main",
            "ctextinct-train=ctextinct.train",
            "ctextinct-parse=ctextinct.parse_and_forum"
        ]
    },
)
