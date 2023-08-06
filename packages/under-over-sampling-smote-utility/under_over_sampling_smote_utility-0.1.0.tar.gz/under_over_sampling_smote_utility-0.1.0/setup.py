from setuptools import find_packages, setup

setup(
    name="under_over_sampling_smote_utility",
    version="0.1.0",
    author="Monika N",
    description="""Package containing utilities to undersample and over sample data set. """,
    packages=find_packages(),
    tests_require=[
        "pytest",
        "pytest-cov",
    ],
    install_requires=[
        "scikit-datasets",
        "sklearn",
        "imblearn",
        "pyyaml",
    ],
    package_data={
        "over_under_sampler": ["resources/*"]
    },
)
