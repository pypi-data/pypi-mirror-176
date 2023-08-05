# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Switch Automation Pty Ltd.",
    description="A package for helping with the creation of Platform Guides in Switch Automation Platform.",
    long_description=open('README.md', 'r').read() + '\n\n' + open('HISTORY.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    name="switch_guides_scaffold",
    version="0.1.4",
    packages=find_packages(
        include=["switch_guides_scaffold", "switch_guides_scaffold.*"],
        exclude=["switch_guides_scaffold.tests", "switch_guides_scaffold.tests.*"]
    ),
    install_requires=['switch-guides', 'click', 'click-help-colors', 'click_spinner', 'pydantic==1.9.0', 'jinja2'],
    python_requires=">=3.8.*",
    entry_points={
        'console_scripts': [
            'swag=switch_guides_scaffold.cli:cli',
            'switchguides=switch_guides_scaffold.cli:cli'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Other Audience',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Natural Language :: English',
    ]
)
