git-smudge
==========

A powerful filter driver for Git which can automatically apply local changes to the
working tree of a repository.

## Installing

Run

    $ pip3 install git-smudge

## Setting up a filter

There are two steps to setting up a filter in your repository. The first is to define the
filter using `git config` and the second is to apply the filter to specific files using
`.git/info/attributes`.

> Note: All commands here are assuming you're using `bash` or another Bourne-like
> shell. If you're using Windows, you should have `GIT Bash` installed.

```sh
$ git config filter.replacename.process 'git-smudge --process --simple "Firefox" "Katiefox"'

$ echo *.cpp filter=replacename >> .git/info/attributes
```

> Note: You could technically use `.gitattributes`, but since that file usually gets
> checked into the repo, it's not good to put local settings there.

## TODO: More documentation here
