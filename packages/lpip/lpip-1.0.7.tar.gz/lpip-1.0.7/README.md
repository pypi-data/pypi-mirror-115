# LocalPIP/LPIP

LocalPIP is an offline package manager for Python...\
 It solves packages dependencies conflict issues and compiling errors.\
 Internet access is required only for the first time of downloading LocalPIP repository.\
 Once downloaded, you can install packages completely offline.

## LocalPIP/LPIP initialization:

| Description                                   | Command               |
| :-------------------------------------------- | :-------------------- |
| To install LocalPIP                           | `pip install lpip -U` |
| To download the local repo for the first time | `lpip download`       |
| To update the local repo                      | `lpip update`         |
| To delete the local repo                      | `lpip delete`         |
| About localpip                                | `lpip about`          |

## Usage

`lpip <Action> <PackageName>`\
`lpip <Action> <PackageName1> <PackageName2>`

| Description | Command                        |
| :---------- | :----------------------------- |
| Actions     | install / uninstall / upgrade  |
| PackageName | one package / multiple package |

## Packages management (`localpip` can be used instead of `lpip`)

| Description                     | Command                              |
| :------------------------------ | :----------------------------------- |
| To install one package          | `lpip install pandas`                |
| To install multiple packages    | `lpip install pandas openpyxl Keras` |
| To install requirement file     | `lpip install req`                   |
| To uninstall a package          | `lpip uninstall pandas`              |
| To upgrade a package            | `lpip upgrade pip`                   |
| To onlone upgrade a package     | `lpip onlineupgrade pip`             |
| To uninstall a package          | `lpip uninstall pandas`              |
| To check all installed packages | `lpip list`                          |

## Current available packages:

[LocalPIP Packages](https://github.com/alexbourg/LocalPIP)
