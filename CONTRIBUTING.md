# Contributing

Contributions of all kinds are welcome here, and they are greatly appreciated!
Every little bit helps, and credit will always be given.


### Report Bugs

Report bugs at https://github.com/UBC-MDS/DSCI-532_2026_29_healthy-diet/issues.

**If you are reporting a bug, please follow the template guidelines. The more
detailed your report, the easier and thus faster we can help you.**

### Fix Bugs

Look through the GitHub issues for bugs. Anything labelled with `bug` and
`help wanted` is open to whoever wants to implement it. When you decide to work on such
an issue, please assign yourself to it and add a comment that you'll be working on that,
too. If you see another issue without the `help wanted` label, just post a comment, the
maintainers are usually happy for any support that they can get.

### Implement Features

Look through the GitHub issues for features. Anything labelled with
`enhancement` and `help wanted` is open to whoever wants to implement it. As
for [fixing bugs](#fix-bugs), please assign yourself to the issue and add a comment that
you'll be working on that, too. If another enhancement catches your fancy, but it
doesn't have the `help wanted` label, just post a comment, the maintainers are usually
happy for any support that they can get.

### Write Documentation

BeautifulNumbers could always use more documentation, whether as
part of the official documentation, in docstrings, or even on the web in blog
posts, articles, and such. Just
[open an issue](https://github.com/UBC-MDS/DSCI-532_2026_29_healthy-diet/issues)
to let us know what you will be working on so that we can provide you with guidance.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/UBC-MDS/DSCI-532_2026_29_healthy-diet/issues. If your feedback fits the format of one of
the issue templates, please use that. Remember that this is a volunteer-driven
project and everybody has limited time.

## Get Started!

Ready to contribute? Here's how to set up BeautifulNumbers for
local development.

1. Fork the https://github.com/UBC-MDS/DSCI-532_2026_29_healthy-diet
   repository on GitHub.
2. Clone your fork locally (*if you want to work locally*)

    ```shell
    https://github.com/UBC-MDS/DSCI-532_2026_29_healthy-diet/issues
    ```
   
3. Create a branch for local development using the default branch (typically `main`) as a starting point. Use `fix` or `feat` as a prefix for your branch name.

    ```shell
    git checkout main
    git checkout -b fix-name-of-your-bugfix
    ```

    Now you can make your changes locally.

4. Commit your changes and push your branch to GitHub. Please use [semantic
   commit messages](https://www.conventionalcommits.org/).

    ```shell
    git add .
    git commit -m "fix: summarize your changes"
    git push -u origin fix-name-of-your-bugfix
    ```

5. Open the link displayed in the message when pushing your new branch in order
   to submit a pull request.

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your
   new functionality into a function with a docstring.
3. Your pull request will automatically be checked by the full test suite.
   It needs to pass all of them before it can be considered for merging.

## M3 retrospective

## What worked well

- Decent pull request hygiene by configuring branch protection rules that required at least one reviewer before merging into the dev branch.
- Used exclusive branches for task.


## What did not work well

- Need more communication through GitHub issues and team check ins, which could help clarify requirements and ensure steady progress toward milestone goals.
- We had some dirty branches (branches were sometimes not rebased or cleaned before opening a PR), which makes the `git diff` harder to read.
- Did not complete relevant `CHANGELOG.md` additions/changes with each PR.
- Issues with final merge conflicts when pushing to main always seem to slow things down before submission. Better file management and commit isolation could be beneficial.

## M4 Collaboration norms

We agreed on:
- Work on improvements right away and let the team know about them in order to fix the critical issues of the dashboard.
- Prioritise specification and design discussions before beginning the code and implementation of improvements.
- Break down complex features into modular tasks with low dependencies.
- Improve communication through Github issues.
- Implement detailed review on PR's assigned to the person.
- Enforced deletion of branches once PR's merged.

