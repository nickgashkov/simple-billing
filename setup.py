from pathlib import Path
from typing import List

from setuptools import find_packages, setup


def requires(name: str) -> List[str]:
    root = Path(__file__).parent
    filepath = root.joinpath(name)

    return [line for line in filepath.read_text().splitlines() if line]


setup(
    name='Simple Billing',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires('requirements/base.txt'),
    extras_require={'dev': requires('requirements/dev.txt')},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'billing-api = billing.api.__main__:main',
        ]
    },
)
