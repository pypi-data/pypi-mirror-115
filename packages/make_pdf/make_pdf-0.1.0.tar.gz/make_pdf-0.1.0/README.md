[![Build Status](https://drone.eorlbruder.de/api/badges/EorlBruder/make_pdf/status.svg)](https://drone.eorlbruder.de/EorlBruder/make_pdf)

A command line tool to convert files to fancy PDFs.

This tool generates nice-looking reports, letters, presentations etc. from Markdown. Other formats also work, but aren't really supported. The only Output format is PDF.

You can use custom themes with customizable fonts, logos and names. 

# Installation

0. Install all requirements:
    - python (at least 3.6) and pip
    - texlive with certain modules (texlive-most on archlinux works for me)
    - pandoc (Only on Linux and then it depends on how you installed pypandoc and if pandoc came bundled with that)
2. Clone this repository: `git clone https://git.eorlbruder.de/EorlBruder/mdp2df.git`
3. Install with pip: `pip install .`

# Usage

By default, this tool only requires an input-file. Thus, the following command works as a minimal example:

```bash
make_pdf test.md
```

This command will create a `test-final.pdf`-file. 

You'll get a bunch more information with `make_pdf --help`.

# Contribute

To see how to contribute please have a look at the CONTRIBUTING.md-file.
