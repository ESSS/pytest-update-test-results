import io

import setuptools

with io.open("CHANGELOG.rst", encoding="UTF-8") as changelog_file:
    history = changelog_file.read()

requirements = ["pytest"]
extras_require = {
    "docs": ["sphinx >= 1.4", "sphinx_rtd_theme", "sphinx-autodoc-typehints"],
    "testing": ["pytest", "pre-commit", "tox"],
}
setuptools.setup(
    author="ESSS",
    author_email="foss@esss.co",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Pytest",
    ],
    description="Pytest plugin to change XML files from a previous run.",
    extras_require=extras_require,
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    python_requires=">=3.6",
    keywords="pytest",
    name="pytest-merge-xml",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    url="http://github.com/ESSS/pytest-merge-xml",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    zip_safe=False,
    entry_points={"pytest11": ["pytest-merge-xml = pytest_merge_xml.plugin"]},
)
