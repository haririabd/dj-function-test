import shutil
from pathlib import Path

# CONFIGURATION
APP_NAME = "emailer"
SRC_PATH = Path("src") / APP_NAME
TARGET_PATH = Path("../publish") / APP_NAME

# Ensure target folder is clean
if TARGET_PATH.exists():
    shutil.rmtree(TARGET_PATH)
TARGET_PATH.parent.mkdir(exist_ok=True)

# Copy app folder
shutil.copytree(SRC_PATH, TARGET_PATH)
print(f"✅ Copied {APP_NAME} to {TARGET_PATH}")

# Create setup.py
setup_code = f"""from setuptools import setup, find_packages

setup(
    name='django-{APP_NAME}',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'python-dotenv>=1.0',
        'requests>=2.25',
    ],
    description='Reusable Django email backend for ZeptoMail',
    author='Hariri A.',
    author_email='hariri.bin.abdullah@gmail.com',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
"""
Path(TARGET_PATH.parent / "setup.py").write_text(setup_code)
print("✅ Created setup.py")

# Create MANIFEST.in
manifest_code = f"""include README.md
recursive-include {APP_NAME}/templates *
recursive-include {APP_NAME}/static *
recursive-include {APP_NAME}/management *
"""
Path(TARGET_PATH.parent / "MANIFEST.in").write_text(manifest_code)
print("✅ Created MANIFEST.in")

# Create README.md
readme_code = f"""# django-{APP_NAME}

Reusable Django app for ZeptoMail integration.

## Installation

```bash
pip install git+https://github.com/yourusername/django-{APP_NAME}.git
```

## Setup

```bash
python manage.py setup_emailer
```

## Usage

Add `'emailer'` to `INSTALLED_APPS` and configure `.env` as prompted
"""
Path(TARGET_PATH.parent / "README.md").write_text(readme_code)
print("✅ Created README.md")
print("\n🎉 App is ready for publishing in /publish")