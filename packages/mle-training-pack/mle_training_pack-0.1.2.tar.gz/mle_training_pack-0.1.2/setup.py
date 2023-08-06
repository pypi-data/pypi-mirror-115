from setuptools import find_packages, setup

setup(
    name="mle_training_pack",
    version="0.1.2",
    description="Training on python packaging and testing",
    classifiers=["Development Status :: 3 - Alpha"],
    keywords="MLE Training - Housing",
    url="https://github.com/VenkatakrishnanG/mle-training_2",
    author="VenkatakrishnanG",
    author_email="venkata.govinda@tigeranalytics.com",
    license="TA",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "sklearn",
        "logging_tree",
        "pytest",
        "six",
        "argparse",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "extract_data=mle_training_pack.ingest_data:main",
            "train_model=mle_training_pack.train:main",
            "score_test=mle_training_pack.test:main",
        ]
    },
)
