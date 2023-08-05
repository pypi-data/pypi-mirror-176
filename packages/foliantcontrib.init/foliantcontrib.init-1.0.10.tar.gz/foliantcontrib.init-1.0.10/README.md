[![](https://img.shields.io/pypi/v/foliantcontrib.init.svg)](https://pypi.org/project/foliantcontrib.init/) [![](https://img.shields.io/github/v/tag/foliant-docs/foliantcontrib.init.svg?label=GitHub)](https://github.com/foliant-docs/foliantcontrib.init)

# Project Initializer for Foliant

This CLI extension add `init` command that lets you create Foliant projects from templates.


## Installation

```shell
$ pip install foliantcontrib.init
```


## Usage

You can create a project from the default _base_ template or from a custom template

### Base template

Create project from the default _base_ template:

```shell
$ foliant init
Enter the project name: Awesome Docs
✔ Generating Foliant project
─────────────────────
Project "Awesome Docs" created in awesome-docs
```

### Custom template

You can load a custom template from a local path or from a git repo

#### Custom template from a local path

```shell
$ foliant init --template /path/to/custom/template
Enter the project name: Awesome Customized Docs
✔ Generating Foliant project
─────────────────────
Project "Awesome Customized Docs" created in awesome-customized-docs
```

#### Custom template from a git repository


```shell
$ foliant init --template https://github.com/path/to/custom/template
Enter the project name: Awesome Docs from git
────────────────────
Project "Awesome Docs from git" created in awesome-docs-from-git
```

### Other options

You can provide the project name without user prompt:

```shell
$ foliant init --name Awesome Docs
✔ Generating Foliant project
─────────────────────
Project "Awesome Docs" created in awesome-docs
```

Another useful option is `--quiet`, which hides all output except for the path to the generated project:

```shell
$ foliant init --name Awesome Docs --quiet
awesome-docs
```

To see all available options, run `foliant init --help`:

```shell
$ foliant init --help
usage: foliant init [-h] [-n NAME] [-t NAME, PATH or git-repo] [-q] [-d]

Generate a new Foliant project.

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of the Foliant project.
  -t NAME, PATH or git-repo, --template NAME, PATH or git-repo
                        Name of a built-in project template or path to custom one.
  -q, --quiet           Hide all output accept for the result. Useful for piping.
  -d, --debug           Log all events during project creation. If not set, only warnings and errors are logged.
```


## Project Templates

A project template is a regular Foliant project but maybe containing placeholders in files. When the project is generated, the placeholders are replaced with the values you provide. Currently, there are two placeholders: `$title` and `$slug`.

There is a built-in template called `base`. It's used by default if no template is specified.
