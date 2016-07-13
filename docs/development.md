Development Model
====================

This document explains the development model used in this project. It is
vaguely inspired by the git flow model (see the "Related models" section).

## The branching strategy

As with most git repositories, there are 2 main branches that will always
exist:

  - `master`
  - `develop`

The code at `HEAD` in `origin/master` is the latest stable code (considered
production-ready).

Similarly `HEAD` in `origin/develop` contains the latest version of the code
that's under development. Once the code in `origin/develop` is stable, we
create a pull request to master, which is then merged using GitHub's interface
or using `git merge --no-ff`; we want to have a merge commit so we can easily
revert merges.


### Feature branches

Work on features should happen in `feature/*` branches which branch off the
latest `develop`.

    $ git checkout -b feature/some-feature develop

Once the feature is completed, push your feature branch to the main repository,
and open a pull request against `origin/develop`.

Once the pull request is approved, it will be merged using GitHub's interface
(so that we get a merge commit and everyone knows it happened).


### Fixes

If there is an important bug in `master` that needs to be fixed and it can't
wait for `develop` to be stable, create a `hotfix/*` branch off `master`,
commit your fix, push it, and then create 2 pull requests: one against `master`
and one against `develop`. This avoids us having to merge `master` into
`develop` and then having a confusing git log; we'll have a `merge
hotfix/bug-name into develop` which is going to be clear instead of having
`merge master into develop` and people wondering "why did that happen?".


## Code reviews

Before your branch can be merged into the `develop` branch, it needs to be
reviewed. This includes general comments about the implementation as well as
more specific things like code style improvements and typos. Merges can only
happen with a "looks good to me" from whoever's supposed to say that for that
specific pull request.

To prepare your pull request, you may need to re-order, modify, or squash some
commits from your branch to have a coherent chain of commits that clearly
explain the development process of the feature. Please do this before pushing
your branch, as we want to avoid force-pushing. If you've already pushed your
branch to the main repository, you can delete the old remote branch, rename
your local branch, rebase, and then push the "new" branch. The rename is to
avoid conflicts if someone else checked out that branch.

If you need to make changes based on code review suggestions, add new commits
to the branch, with subject lines which explain what the commit does just like
regular commits, but mention the pull request number in the body of the commit
message so that people reading the git log will be able to find the discussion
that led to the commit. This can either be a full link to the pull request, or
just `#49` since GitHub will automatically make that a link.


## Style checks

Before pushing your changes (but ideally before every commit), make sure you've
run `pycodestyle` and `pyflakes` (or `flake8` which wraps both) on your code
and fixed the reported issues. So you don't forget, add it as a pre-commit
hook, or even better, look into how your editor can run them automatically on
save. Vim users can use the `python-mode` or `vim-flake8` plugins.


## Writing good commit messages

The general consensus on good git commit messages is the following format
(copied from Tim Pope's [blog
post](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html) on
the subject):

```
Capitalized, short (50 chars or less) summary

More detailed explanatory text, if necessary.  Wrap it to about 72
characters or so.  In some contexts, the first line is treated as the
subject of an email and the rest of the text as the body.  The blank
line separating the summary from the body is critical (unless you omit
the body entirely); tools like rebase can get confused if you run the
two together.

Write your commit message in the imperative: "Fix bug" and not "Fixed bug"
or "Fixes bug."  This convention matches up with commit messages generated
by commands like git merge and git revert.

Further paragraphs come after blank lines.

- Bullet points are okay, too

- Typically a hyphen or asterisk is used for the bullet, followed by a
  single space, with blank lines in between, but conventions vary here

- Use a hanging indent
```

There's also Chris Beams' [blog post](http://chris.beams.io/posts/git-commit/)
which contains the same suggestions, but goes into a lot more detail and
justifies all the "rules".


## Git tips

The following are a few tips on using git that are relevant to this document.


### You don't have to push

Remember, git is a _distributed_ version control system, and this means you
don't have to push your commits to the remote repository. It also means you can
push commits to any other clone of the main repository, which is useful if you
want to have a "backup" of your local repository while still being able to
rebase your branch/commits.


### Rebasing

Rebasing in git will take a series of commits (usually you'll use this with
your branch) and re-applies them on top of the specified head. You can run this
interactively to re-order, squash, and modify existing commits.

An example of non-interactive usage is

    $ git rebase develop feature/my-feature

This will take all the commits from `feature/my-feature` and re-apply them on
top of the current `develop`. This is effectively changing the base of your
branch (hence the name).

You can also run this interactively while you're in your `feature/*` branch

    $ git rebase -i develop

This should open up a text editor with a list of commands, commit hashes, and
commit messages and some instructions at the bottom about what you can do.

More info: https://help.github.com/articles/about-git-rebase/


### Force-pushing safely

**Note:** While it may be fine for other repositories (e.g. your own clones of
this repository), we want to avoid force-pushing to this repository as much as
possible. It is only acceptable when there is _no other option_ (e.g. if we
need to remove any trace of a file), and even then, only with the permission of
the owner/maintainer of the project.

Force-pushing ensures the commits on the remote branch match what you have
locally. This is only necessary if the two branches have diverged (git will
tell you this if you try to do a regular push).

When you modify commits, you are also changing their hashes, so other people
who have checked out a copy of your branch will not be able to easily get the
new commits; they'll have to delete their local copy first.

This is not an issue, however, if only one person works per feature branch.
Everyone else who has a copy can delete it (and probably will once it gets
merged anyways).

First thing to be careful about is that you're pushing the correct branch! It's
_highly_ recommended to set `push.default` to `simple` (default in version 2.0):

    $ git config --global push.default simple

Then you can run `git push --force`, but it's a lot safer to be specific about
the branch names (and tab complete should work here):

    $ git push --force origin feature/my-feature:feature/my-feature


### And many more

There are a ton of "git tips" blog posts online, and it's redundant to repeat
everything here, but some more general tips:

* Read the man pages for the commands you're running. They're very well
  written, and have plenty of examples.
* For any issue you have, there's a question on StackOverflow about it.
* If you're doing something that may be error-prone, or may cause you to lose
  information, make a copy of your project repo first.
* Use `gitk` to view your history.
* Set `git config --global push.default simple`
* Set `git config --global merge.conflictstyle diff3`


## Related models

Although we don't use this model, Vincent Driessen's [git flow
model](http://nvie.com/posts/a-successful-git-branching-model/) is a very good
read for workflow ideas and git tips. There's also a related git extension:
https://github.com/nvie/gitflow
