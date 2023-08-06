# LocalPIP

LocalPIP is an offline package manager for Python...\
 It solves packages dependencies conflict issues and compiling errors.\
 Internet access is required only for the first time of downloading LocalPIP repository.\
 Once downloaded, you can install packages completely offline.

## LocalPIP initialization:

| Description                                   | Command                |
| :-------------------------------------------- | :--------------------- |
| To install LocalPIP                           | `pip install localpip` |
| To download the local repo for the first time | `localpip download`    |
| To update the local repo                      | `localpip update`      |
| About localpip                                | `localpip about`       |

## Usage

`localpip <Action> <PackageName>`\
`localpip <Action> <PackageName1> <PackageName2>`

| Description | Command                        |
| :---------- | :----------------------------- |
| Actions     | install / uninstall / upgrade  |
| PackageName | one package / multiple package |

## Packages management (`lpip` can be used instead of `localpip`)

| Description                     | Command                                  |
| :------------------------------ | :--------------------------------------- |
| To install one package          | `localpip install pandas`                |
| To install multiple packages    | `localpip install pandas openpyxl Keras` |
| To install requirement file     | `localpip install req`                   |
| To uninstall a package          | `localpip uninstall pandas`              |
| To upgrade a package            | `localpip upgrade pip`                   |
| To onlone upgrade a package     | `localpip onlineupgrade pip`             |
| To uninstall a package          | `localpip uninstall pandas`              |
| To check all installed packages | `localpip list`                          |

## Current available packages:

[LocalPIP Packages](https://github.com/alexbourg/LocalPIP)
