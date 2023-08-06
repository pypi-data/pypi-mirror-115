from setuptools import setup, find_packages

setup(
    name="safegate-pro-frontend",
    version="20210805.0",
    description="The Safegate Pro frontend",
    url="https://github.com/home-assistant/home-assistant-polymer",
    author="The Safegate Pro Authors",
    author_email="hello@home-assistant.io",
    license="Apache-2.0",
    packages=find_packages(include=["hass_frontend", "hass_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)
