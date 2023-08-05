import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pete_tpl",
    version="0.5.1",
    author="Serg",
    author_email="1899416+dontpullthis@users.noreply.github.com",
    description="A Jinja-like template engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pete-tpl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'requests',  # it's needed only for scripts. Could it be replaced with something else?
    ],
    python_requires='>=3.6',
    scripts=['scripts/petetpl_postinstall.py'],
)
