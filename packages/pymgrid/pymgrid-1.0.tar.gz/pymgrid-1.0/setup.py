from setuptools import setup, find_packages

EXTRAS = dict()
EXTRAS["genset_mpc"] = ["Mosek", "cvxopt"]
EXTRAS["dev"] = ["pytest", "flake8", *EXTRAS["genset_mpc"]]
EXTRAS["all"] = list(set(sum(EXTRAS.values(), [])))

setup(
    name="pymgrid",
    package_dir={"": "src"},
    packages=find_packages("src"),
    version="1.0",
    python_requires=">=3.0",
    download_url="https://github.com/Total-RD/pymgrid/archive/refs/tags/v1.0-beta.tar.gz",
    include_package_data=True,
    install_requires=[
        "requests",
        "pandas",
        "numpy",
        "cvxpy",
        "statsmodels",
        "matplotlib",
        "plotly",
        "cufflinks",
        "gym",
        "tqdm",
        "pyyaml"
    ],
    extras_require=EXTRAS
)
