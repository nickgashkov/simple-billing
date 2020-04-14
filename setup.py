from pathlib import Path
from typing import List

from setuptools import find_packages, setup


def version() -> str:
    root = Path(__file__).parent
    filepath = root / 'billing' / 'version.txt'

    return filepath.read_text().strip()


def requires(name: str) -> List[str]:
    root = Path(__file__).parent
    filepath = root.joinpath(name)

    return [line for line in filepath.read_text().splitlines() if line]


setup(
    name='Simple Billing',
    version=version(),
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
