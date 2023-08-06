# Contributing to MAKE-PDF

First I want to thank you for considering contributing to this project! 

Now we have a slight problem for now. I'm hosting this project on my private gogs-instance, and I'm actually not a super huge fan of just opening registrations here. On the other hand - without forge-federation I'm fully aware of it not being possible to contribute here. I've closed registration for now.

So here are the possibilities for contributing atm:

- If your contribution is the reporting of a bug or a feature-request, you can also contact me, and I'll be creating the issue in the tracker. 
- Same goes for small changes
- Now if you want to fork the project and create PRs, you can clone it and send me a patch via e-mail. 

To contact me you can e-mail me to <eorl@bruder.space>.

Nonetheless, I'll document the workflow for contributions etc. below.

## Creating an issue

If you're creating an issue in the issue-tracker please try being precise about what you want to achieve. Consider the following questions:

- What category does my question fall in? Am I reporting a bug, asking for a feature, is a translation faulty?
    - There might be one or more fitting labels for the category. Feel free to use them.
- What is the current state? What should be changed?
- How might this impact the program?

It's totally okay, if oyu can't answer those questions, if something's unclear I'll probably ask :)


## Typical workflow for a contribution

0. Fork the project if you did not already or if you do not have access to the main repository
1. Checkout the master branch and pull most recent changes: git checkout master && git pull
2. If working on an issue, assign yourself to the issue. Otherwise, consider open an issue before starting to work on something, especially for new features.
3. Create a dedicated branch for your work 42-awesome-fix. It is good practice prefixing your branch name with the ID of the issue you are solving.
4. Work on your stuff
5. Commit small, atomic changes to make it easier to review your contribution
6. Add a changelog fragment to summarize your changes: echo "Implemented awesome stuff (#42)" > changes/changelog.d/42.feature
7. Push your branch
8. Create your merge request
9. Take a step back and enjoy, we're really grateful you did all of this and took the time to contribute!


## Changelog management


To ensure we have extensive and well-structured changelog, any significant work such as closing an issue must include a changelog fragment. Small changes may include a changelog fragment as well but this is not mandatory. If you're not sure about what to do, do not panic, open your merge request normally, and we'll figure everything during the review ;)

Changelog fragments are text files that can contain one or multiple lines that describe the changes occurring in a bunch of commits. Those files reside in `changes/changelog.d`.

### Content

A typical fragment looks like that:

> Fixed broken audio player on Chrome 42 for ogg files (#567)

If the work fixes one or more issues, the issue number should be included at the end of the fragment ((#567) is the issue number in the previous example).

If your work is not related to a specific issue, use the merge request identifier instead, like this:

> Fixed a typo in landing page copy (!342)

### Naming 

Fragment files should respect the following naming pattern: `changes/changelog.d/<name>.<category>`. Name can be anything describing your work, or simply the identifier of the issue number you are fixing. Category can be one of:

- `feature`: for new features
- `enhancement`: for enhancements on existing features
- `bugfix`: for bugfixes
- `doc`: for documentation 
- `i18n`: for internationalization-related work 
- `misc`: for anything else

### Shortcuts

Here is a shortcut you can use/adapt to easily create new fragments from command-line:

```bash
issue="42"
content="Fixed an overflowing issue on small resolutions (#$issue)"
category="bugfix"
echo "$content ($issue)" > changes/changelog.d/$issue.$category
```

You can of course create fragments by hand in your text editor, or from Gitlab's
interface as well.

## Internationalization

We use gettext for making sure our output (especially the help-messages) are translated. While coding this mainly means that you should wrap those string in `_(string)` and import `_` from make_pdf. 

When you add a string, please notify the translation team (best via your issue on gogs) about it or add translations by yourself.

To ease the workflow we use `pybabel`, which provides some ease of use tooling and comes with our dev-dependencies.

1. Extract the messages from the source files with `pybabel extract -o ./src/make_pdf/resources/locales/base.pot ./src`
2. Then update the locale-files with the newly added strings `pybabel update -i ./src/make_pdf/resources/locales/base.pot -D base -d ./src/make_pdf/resources/locales`
3. Then add the translations in the `base.po`-files for all languages
4. Finally, you need to compile the translations with `pybabel compile -D base -d ./src/make_pdf/resources/locales`



## Creating a new release

To make a new 3.4 release:

```bash
# setup
export NEXT_RELEASE=3.4  # replace with the next release number
export PREVIOUS_RELEASE=3.3  # replace with the previous release number

# ensure you have an up-to-date repo
git checkout master
git pull

# compile changelog
towncrier --version $NEXT_RELEASE --yes

# polish changelog
# - update the date
# - look for typos
# - add list of contributors via `python3 scripts/get-contributions-stats.py develop $PREVIOUS_RELEASE`
vim CHANGELOG

# Set the `version` variable to $NEXT_RELEASE
vim pyproject.toml

# commit
git add .
git commit -m "Version bump and changelog for $NEXT_RELEASE"

# tag
git tag $NEXT_RELEASE

# publish
git push --tags && git push
```

## Set up dev-environment

Now this is pretty much up to you. I'll document what I personally do. 

1. Import the project into PyCharm. 
2. Create the venv with `python -m venv ./venv --clear`
3. Activate the venv `. ./venv/bin/activate`
4. Set PyCharms interpreter to `./venv/bin/python`
5. Install the dev-environment: `pip install .\[dev\]`
   1. Start the black-daemon (either via run-config or from terminal): `./venv/bin/blackd`
   2. Install the [BlackConnect](https://plugins.jetbrains.com/plugin/14321-blackconnect) Plugin
6. If you want to use any of the extras like for example tests run `.pip install .\[test\]` and replace "test" with the desired feature
7. Add run-configs for the desired tasks

This should have set up the environment as needed.

## Build a local version

To build a local version just run `./venv/bin/pip install .`

## Coding guidelines

You should format the code with [black](https://black.readthedocs.io/en/stable/). No further configuration is needed for it.

Regarding unit-tests please write unit-tests for your feature if applicable. Also, run the tests before committing.

Also don't forget your changelog-fragment!