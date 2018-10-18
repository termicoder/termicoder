# Help Texts
### output of all termicoder help commads is pasted here for refrence and documentation.

# Help
```
termicoder --help
termicoder <COMMAND> --help
```

# Basic
```
Usage: termicoder [OPTIONS] COMMAND [ARGS]...

  __       __                      _                __
  \ \     / /____  _________ ___  (_)________  ____/ /__  _____
   \ \   / __/ _ \/ ___/ __ `__ \/ / ___/ __ \/ __  / _ \/ ___/
   / /  / /_/  __/ /  / / / / / / / /__/ /_/ / /_/ /  __/ /
  /_/   \__/\___/_/  /_/ /_/ /_/_/\___/\____/\__,_/\___/_/

  view, code & submit problems directly from terminal.

Options:
  --version            Show the version and exit.
  -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  -h, --help           Show this message and exit.

Commands:
  clip    Copies code from file to clipboard.
  code    Creates and opens file with template code.
  config  Configure settings, autocomplete etc.
  debug   Launches custom debug interface.
  list    List the contents of current folder.
  repl    Start an interactive shell.
  setup   Sets up problem, contests and login.
  submit  Submit a solution.
  test    Test code against the sample testcases.
  view    View contests and problems.
```
## Clip
```
Usage: termicoder clip [OPTIONS] [CODE_FILE]

  Copies code from CODE_FILE to the clipboard.

  If CODE_FILE is not passed, a default file is suggested based on current
  directory.

  The suggested file is the most recently edited code file recognized by
  termicoder.

Options:
  -h, --help  Show this message and exit
```
---
## Code
```
Usage: termicoder code [OPTIONS] [CODE_FILE]

  Creates and opens CODE_FILE with template code.

  If CODE_FILE already exists, 'code' just opens it in the default/
  supplied editor without any change.

  If CODE_FILE is not passed, a default name of file is suggested based on
  current directory, language preferences and existing files in directory.

  Default CODE_FILE is <PROBLEM_NAME>.<DEFAULT_EXTENSION> if user is in a
  problem folder and no other supported code file exists.

  TODO [WIP]: If other code file(s) exist, it should suggests to open the
  most recently edited one.

  Template for the code is loaded based upon extension.

  See 'termicoder config' for editing default templates, editor, and
  language preferences.

Options:
  --editor TEXT  Specify the editor to launch the file with.
  -h, --help     Show this message and exit.
```
---
## Debug
```
Usage: termicoder debug [OPTIONS]

  Launches custom debug interface. Here you can use testcase generator,
  launch debugger for the particular language and visualize the output.

  NOTE: This functionality is not implemented in this version. This option
  is only included for compatibility purposes. If you want to contribute to
  its development visit: https://github.com/termicoder/termicoder

Options:
  -h, --help  Show this message and exit
```
---
## Config
```
Usage: termicoder config [OPTIONS] COMMAND [ARGS]...

  Configure settings, autocomplete etc.

Options:
  -h, --help  Show this message and exit.

Commands:
  autocomplete  Shell completion for termicoder.
  edit          Edit the configuration.
  init          Initialize the config directory.
  man           Setup man pages.
  remove        Remove the configuration directory.
```

### config autocomplete
```
Usage: termicoder config autocomplete [OPTIONS] COMMAND [ARGS]...

  Shell completion for termicoder.

  Available shell types:

    bash         Bourne again shell
    fish         Friendly interactive shell
    powershell   Windows PowerShell
    zsh          Z shell
  Default type: auto

Options:
  -h, --help  Show this message and exit.

Commands:
  install  Install the click-completion-command...
  show     Show the click-completion-command completion...
```

#### config autocomplete install
```
Usage: termicoder config autocomplete install [OPTIONS] [SHELL] [PATH]

  Install the click-completion-command completion

Options:
  --append / --overwrite          Append the completion code to the file
  -i, --case-insensitive / --no-case-insensitive
                                  Case insensitive completion
  -h, --help                      Show this message and exit.
```

#### config autocomplete show
```
Usage: termicoder config autocomplete show [OPTIONS] [SHELL]

  Show the click-completion-command completion code

Options:
  -i, --case-insensitive / --no-case-insensitive
                                  Case insensitive completion
  -h, --help                      Show this message and exit.
```

### config edit
```
Usage: termicoder config edit [OPTIONS]

  Edit the configuration.

  Launches the config folder for modifying settings.

Options:
  -h, --help  Show this message and exit.
```

### config init
```
Usage: termicoder config init [OPTIONS]

  Initialize the config directory.

Options:
  -h, --help  Show this message and exit.
```

### config man
```
Usage: termicoder config man [OPTIONS]

  Setup man pages.

Options:
  -h, --help  Show this message and exit.
```

### config remove
```
Usage: termicoder config remove [OPTIONS]

  Remove the configuration directory.

Options:
  -h, --help  Show this message and exit.
```
---

## List (list is like `view` except all things are done in terminal using paged output)

```
Usage: termicoder list [OPTIONS] COMMAND [ARGS]...

  List the contents of current folder.

Options:
  -h, --help  Show this message and exit.

Commands:
  folder*  View contents of folder.
  contest  List a particular contest.
  running  View all running contests.
```

### list folder* (default commamd: i.e `termicoder view` without subcommand aliases to this) 
```
Usage: termicoder list folder [OPTIONS] [FOLDER]

  display the termicoder contents in current/passed folder
  default folder is current folder.
  if it is a contest folder it displays the list of problems.
  if its a problem folder, displays the problem in a browser.

Options:
  -h, --help  Show this message and exit.

```

### list contest
```
Usage: termicoder list contest [OPTIONS]

  List problems from a particular contest with their status.

  depending on judge it may give a list of categories also such as PRACTICE
  etc.

Options:
  -j, --judge [codechef]
  -h, --help              Show this message and exit.
```

### list running
```
Usage: termicoder list running [OPTIONS]

  View all running contests.

Options:
  -j, --judge [codechef]
  -h, --help              Show this message and exit.
```
---

## REPL
```
Usage: termicoder repl [OPTIONS]

  Start an interactive shell. All commands and subcommands are available in
  it.

  If stdin is not a TTY, no prompt will be printed, but only commands read
  from stdin.

Options:
  -h, --help  Show this message and exit.
```
---


## Setup
```
Usage: termicoder setup [OPTIONS]

  sets up problem, contests and login.

  1. if you pass judge and --login/--logout, it logs you in and out of the
  judge

  2. if you pass judge and contest/category it downloads all the problems of
  that contest.

  3. if you pass a particular problem, with judge and contest/category, it
  sets up that problem.

  all this happens in the current folder. option of contest/category may
  vary amongst various online judges

Options:
  -j, --judge [codechef|iarcs]
  -c, --contest TEXT            contest code
  -p, --problem TEXT            problem code
  --login
  --logout
  --help                        Show this message and exit.
```
---

## Submit (Implementation of submit depends on the judge. It may be terminal or browser based)
```
Usage: termicoder submit [OPTIONS] [CODE_FILE]

  Submit a solution.

  You should be in a problem directory to submit

  Script will prompt you to login into the judge(if not already).

Options:
  -h, --help  Show this message and exit.
```
---
## Test
```
Usage: termicoder test [OPTIONS] [CODE_FILE]

  Test code against the sample testcases.

  this command (compiles and) runs passed code file.
  the code is run against all [.in] files in ./testcases folder.
  the output is produced in [.out] files and checked against [.ans] files

  it displays time for each testcase,status and diff of expected and
  produced outputs.

Options:
  -tl, --timelimit FLOAT  the max time per testcase
  -l, --live              test the code live and don't use testcases
  -h, --help              Show this message and exit.
```
---
## View
```
Usage: termicoder view [OPTIONS] COMMAND [ARGS]...

  View contests and problems.

Options:
  -h, --help  Show this message and exit.

Commands:
  folder*  View contents of folder.
  contest  Display a particular contest
  problem  View a particular problem
  running  View all running contests
```

### folder
```
Usage: termicoder view folder [OPTIONS] [DIR_NAME]

  display the termicoder contents in current/passed folder

  if it is a contest folder it displays the list of problems in the browser.
  if its a problem folder, displays the problem in a browser.

Options:
  --browser TEXT  Browser to launch
  -h, --help      Show this message and exit
```

### contest
```
Usage: termicoder view contest [OPTIONS] [CONTEST_CODE]

  View a contest from the judge (online). Launches the contest in browser.

Options:
  -j, --judge [codechef]
  --browser TEXT          Browser to launch
  -h, --help              Show this message and exit..
```

### problem
```
Usage: termicoder view problem [OPTIONS] PROBLEM_CODE

  View a particular problem from the judge.

Options:
  -j, --judge [codechef]
  -c, --contest TEXT      contest code
  --browser TEXT          Browser to launch
  -h, --help              Show this message and exit.
```

### running
```
Usage: termicoder view running [OPTIONS]

  View all running contests.

Options:
  -j, --judge [codechef]
  --browser TEXT          Browser to launch
  -h, --help              Show this message and exit.
```
---
