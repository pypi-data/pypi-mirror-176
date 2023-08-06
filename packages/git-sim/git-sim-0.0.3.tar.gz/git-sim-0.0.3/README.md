# git-sim
Simulate Git commands on your own repos by generating an image (default) or video visualization depicting the command's behavior. Command syntax is based directly on Git's command-line syntax, so using git-sim is as familiar as possible.

## Use cases
- Visualize Git commands to understand their effects on your repo before actually running them
- Prevent unexpected working directory and repository states by simulating before running
- Share visualizations (jpg image or mp4 video) of your Git commands with your team, or the world
- Save visualizations as a part of your team documentation to document workflow and prevent recurring issues
- Create static Git diagrams (jpg) or dynamic animated videos (mp4) to speed up content creation
- Help visual learners understand how Git commands work

## Features
- Run a one-liner git-sim command in the terminal to generate a custom Git command visualization (.jpg) from your repo
- Supported commands: `status`, `add`, `branch`, `tag`, `reset`, `revert`
- Generate an animated video (.mp4) instead of a static image using the `--animate` flag (note: significant performance slowdown, it is recommended to use `--low-quality` to speed up testing and remove when ready to generate presentation-quality video)
- Choose between dark mode (default) and light mode
- Animation only: Add custom branded intro/outro sequences if desired
- Animation only: Speed up or slow down animation speed as desired

## Commands
Basic usage is similar to Git itself - `git-sim` takes a familiar set of subcommands such as "status", "add", "commit", "branch", "reset", "revert", etc, along with corresponding options.

```console
$ git-sim [global options] <subcommand> [subcommand options]
```

The `[global options]` apply to the overarching `git-sim` simulation itself, including:

`--light-mode`: Use a light mode color scheme instead of default dark mode.
`--animate`: Instead of outputting a static image, animate the Git command behavior in a .mp4 video. 

Animation-only global options (to be used in conjunction with `--animate`:  
`--speed=n`: Set the multiple of animation speed of the output simulation, `n` can be an integer or float, default is 1.  
`--low-quality`: Render the animation in low quality to speed up creation time, recommended for non-presentation use.  
`--show-intro`: Add an intro sequence with custom logo and title.  
`--show-outro`: Add an outro sequence with custom logo and text.  
`--title=title`: Custom title to display at the beginning of the animation.  
`--logo=logo.png`: The path to a custom logo to use in the animation intro/outro.  
`--outro-top-text`: Custom text to display above the logo during the outro.  
`--outro-bottom-text`: Custom text to display below the logo during the outro.

The `[subcommand options]` are like regular Git options specific to the specified subcommand (see below for a full list).

The following is a list of Git commands that can be simulated and their corresponding options/flags.

### git status
Usage: `git-sim status`

- Simulated output will show the state of the working directory, staging area, and untracked files
- Note that simulated output will also show the most recent 5 commits on the active branch

![git-sim-status_11-11-22_22-57-49](https://user-images.githubusercontent.com/49353917/201461977-189d58fd-f796-4069-b94e-dfb5a395758a.jpg)

### git add
Usage: `git-sim add --name=<file>`

- Specify `<file>` as a *modified* working directory file, or an untracked file
- Simulated output will show files being moved to the staging area
- Note that simulated output will also show the most recent 5 commits on the active branch

![git-sim-add_11-11-22_22-59-54](https://user-images.githubusercontent.com/49353917/201461985-2ebf7bfe-929a-4025-9049-8f2a933a237a.jpg)

### git branch
Usage: `git-sim branch --name=<new-branch>`

- Specify `<new-branch>` as the name of the new branch to simulate creation of
- Simulated output will show the newly create branch ref along with most recent 5 commits on the active branch

![git-sim-branch_11-11-22_23-00-36](https://user-images.githubusercontent.com/49353917/201461993-5f5ae510-1b04-4cb3-9002-72e969c4d73a.jpg)

### git tag
Usage: `git-sim tag --name=<new-tag>`

- Specify `<new-tag>` as the name of the new tag to simulate creation of
- Simulated output will show the newly create tag ref along with most recent 5 commits on the active branch

![git-sim-tag_11-11-22_23-00-57](https://user-images.githubusercontent.com/49353917/201461998-86f58c5a-8fb5-4882-bb87-7e42e67d5c37.jpg)

### git reset
Usage: `git-sim reset --commit=<reset-to> [--mixed|--soft|--hard]`

- Specify `<reset-to>` as any commit id, branch name, tag, or other ref to simulate reset to from the current HEAD (default: `HEAD`)
- As with a normal git reset command, default reset mode is `--mixed`, but can be specified as desired using  `--mixed`, `--soft`, or `--hard`
- Simulated output will show branch/HEAD resets and resulting state of the working directory, staging area, and whether any file changes would be deleted by running the actual command

![git-sim-reset_11-11-22_23-02-42](https://user-images.githubusercontent.com/49353917/201462003-bf59e272-16fa-4c3d-b9f3-0fc91d2caa48.jpg)

### git revert
Usage `git-sim revert --commit=<to-revert>`

- Specify `<to-revert>` as any commit id, branch name, tag, or other ref to simulate revert for
- Simulated output will show the new commit which reverts the changes from `<to-revert>`
- Simulated output will include the next 4 most recent commits on the active branch

![git-sim-revert_11-11-22_23-03-14](https://user-images.githubusercontent.com/49353917/201462008-2268a339-4b3b-452a-bd17-9be8d04eeafe.jpg)

## Video animation example
```console
$ git-sim --animate reset --commit=HEAD^
```

https://user-images.githubusercontent.com/49353917/201462192-a3bc3a2e-f2c9-4166-81ce-743e53255fc2.mp4

## Requirements
* Python 3.7 or greater
* Pip (Package manager for Python)
* [Manim (Community version)](https://www.manim.community/)
* GitPython
* OpenCV

## Quickstart
1) Install [manim and manim dependencies for your OS](https://www.manim.community/)

2) Install `git-sim`:

```console
$ pip3 install git-sim
```

3) Browse to the Git repository you want create an animation from:

```console
$ cd path/to/git/repo
```

4) Run the program:

```console
$ git-sim [global options] <subcommand> [subcommand options]
```

5) Simulated output will be created as a `.jpg` file. Output files are named using the subcommand executed combined with a timestamp, and by default are stored in a subdirectory called `git-sim_media/`. The location of this subdirectory is customizable using the command line flag `--media-dir=path/to/output`. Note that when the `--animate` global flag is used, render times will be much longer and a `.mp4` video output file will be produced.

6) See global help for list of global options/flags and subcommands:

```console
$ git-sim -h
```

7) See subcommand help for list of options/flags for a specific subcommand:

```console
$ git-sim <subcommand> -h
```

## Basic command examples
Simulate the output of the git status command:

```console
$ cd path/to/git/repo
$ git-sim status
```

Simulate adding a file to the Git staging area:

```console
$ git-sim --light-mode add --name=filename.ext
```

Simulate creating a new Git branch:

```console
$ git-sim branch --name=new-branch-name 
```

Simulate creating a new Git tag:

```console
$ git-sim tag --name=new-tag-name
```

Simulate a hard reset of the current branch HEAD to the previous commit:

```console
$ git-sim reset --commit=HEAD^ --hard
```

Simulate reverting the changes in an older commit:

```console
$ git-sim revert --commit=HEAD~7
```

## Command examples with extra options/flags
Use light mode for white background and black text, instead of the default black background with white text:

```console
$ git-sim --light-mode status
```

Animate the simulated output as a .mp4 video file:

```console
$ git-sim --animate add --name=filename.ext
```

Add an intro and outro with custom text and logo (must include `--animate`)

```console
$ git-sim --animate --show-intro --show-outro --outro-top-text="My Git Repo" --outro-bottom-text="Thanks for watching!" --logo=path/to/logo.png status
```

Customize the output image/video directory location:

```console
$ git-sim --media-dir=path/to/output status
```

Generate output video in low quality to speed up rendering time (useful for repeated testing, must include `--animate`):

```console
$ git-sim --animate --low-quality status
```

## Installation
See **Quickstart** section for details on installing manim and other dependencies. Then run:

```console
$ pip3 install git-sim
```

## Learn More
Learn more about this tool on the [git-sim project page](https://initialcommit.com/tools/git-sim).

## Authors
**Jacob Stopak** - on behalf of [Initial Commit](https://initialcommit.com)
