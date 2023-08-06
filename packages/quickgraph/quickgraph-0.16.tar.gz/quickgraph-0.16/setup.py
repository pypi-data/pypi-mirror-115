import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name = "quickgraph",
    version = "0.16",
    author = "Mobile Systems and Networking Group, Fudan University",
    author_email = "gongqingyuan@fudan.edu.cn",
    url = "https://gongqingyuan.wordpress.com/",
    description = "QuickGraph library can help you get a quick overview of a social graph in an extremely convenient way. QuickGraph will show the basic information of a graph, plot the CDF of selected metrics, characterize the largest connected component (LCC).",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
