from setuptools import setup, find_packages

setup(
    name='mass-post-office',
    version='0.0.1',
    description="Mass Post Office",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='django, post-office, mass-post-office',
    author='Yaroslav Klyuyev (imposeren)',
    author_email='imposeren@gmail.com',
    url='https://github.com/42cc/mass_post_office',
    packages=find_packages(),
    install_requires=['django-post-office'],
    include_package_data=True,
    zip_safe=False,
)
