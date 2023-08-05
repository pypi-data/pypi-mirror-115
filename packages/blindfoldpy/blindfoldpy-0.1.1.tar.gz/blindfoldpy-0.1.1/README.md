<h1 align="center"> blindfold.py - a lightweight and simple .gitignore generator</h1>

[![Build](https://github.com/iwishiwasaneagle/blindfold.py/actions/workflows/python-build.yml/badge.svg)](https://github.com/iwishiwasaneagle/blindfold.py/actions/workflows/python-build.yml)
[![PyPI](https://img.shields.io/pypi/v/blindfoldpy)](https://pypi.org/project/blindfoldpy/)
[![GitHub license](https://img.shields.io/github/license/iwishiwasaneagle/blindfold.py)](https://github.com/iwishiwasaneagle/blindfold.py/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/iwishiwasaneagle/blindfold.py)](https://github.com/iwishiwasaneagle/blindfold.py/stargazers)

⚠️ This repo is made to annoy my friend [Eoin-McMahon](https://github.com/Eoin-McMahon), the real blindfold is found [here](https://github.com/Eoin-McMahon/blindfold) ⚠️

## ✨ Features
* Pulls .gitignore templates from gitignore.io. 
* Clean and simple CLI
* Allows for the combination of any number of different templates all into one gitignore

## 📦 Installation

#### 📥 Download from pypi.org

```bash
pip install blindfoldpy
```

#### 🏗️ Build from source
```bash
git clone https://github.com/iwishiwasaneagle/blindfold.py
cd blindfold.py
python3 setup.py install
```

## 🔧 Examples of use:
```bash
# generates a single gitignore file for both dart and flutter
blindfoldpy --opts dart flutter
```
<!-- ```bash
# you can specify a specific destination to store the gitignore file using the dest argument
blindfold --lang rust --dest ./src/
``` -->

```bash
# arguments can also be written in shorthand
blindfoldpy -o rust
```

```bash
# shows full list of available templates
blindfoldpy --list
```

```bash
# There is a help screen that can be shown which details the subcommands and arguments to supply to the program
blindfoldpy -h
```
