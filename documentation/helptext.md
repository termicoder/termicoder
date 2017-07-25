# Help Texts
### output of all termicoder help commads is pasted here just for reference before you download.
### after downloading you can always run the [HELP](#help) command

## Help
```
termicoder --help
termicoder <COMMAND> --help
```

## Basic
```
Usage: termicoder [OPTIONS] COMMAND [ARGS]...

  view, code & submit problems directly from terminal.

Options:
  --help  Show this message and exit.

Commands:
  code    creates & open code file with template code.
  debug   launches custom debug interface (in future)...
  setup   sets up problem, contests and login.
  submit  submit a solution.
  test    test code against the sample testcases.
  view    view contests, problems and problem statement
```

## Code
```
Usage: termicoder code [OPTIONS]

  creates & open code file with template code.

  you can edit template code and default editors using flags -et and -ed
  respectively

Options:
  -f, --file PATH        the filename to code into with preloaded template
  -et, --edit_templates  open templates folder
  -ed, --edit_defaults   edit defaults for editors
  --help                 Show this message and exit.
```

## Debug
```
Usage: termicoder debug [OPTIONS]

  launches custom debug interface (in future) where you can use testcase
  generator, launch debugger for the particular language and visualize the
  output

Options:
  --help  Show this message and exit.
```

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

## Submit
```
Usage: termicoder submit [OPTIONS]

  submit a solution.

  you should be in a problem directory to submit

  script will prompt you to login into the judge(if not already).
  this submits the problem using data in [.problem] file in current directory

Options:
  -f, --file FILENAME  the code file
  --help               Show this message and exit.
```

## Test
```
Usage: termicoder test [OPTIONS]

  test code against the sample testcases.

  this command (compiles and) runs passed code file.
  the code is run against all [.in] files in ./testcases folder.
  the output is produced in [.outx] files and checked against [.out] files

  it displays time for each testcase,status and diff of expected and
  produced outputs.

Options:
  -f, --file FILENAME     the code file
  -tl, --timelimit FLOAT  the max time per testcase
  -l, --live              test the code live and don't use testcases
  -es, --edit_scripts
  --help                  Show this message and exit.
```

## View
```
Usage: termicoder view [OPTIONS] COMMAND [ARGS]...

  view contests, problems and problem statement

Options:
  --help  Show this message and exit.

Commands:
  contests  display contest list of a judge
  problems  list problems of a contest/category
  this      view contents of current folder
```

### contests
```
Usage: termicoder view contests [OPTIONS]

  lists current and upcoming contests on a judge.

  depending on judge it may give a list of categories also such as PRACTICE
  etc.

Options:
  -j, --judge [codechef|iarcs]
  --help                        Show this message and exit.
```

### problems
```
Usage: termicoder view problems [OPTIONS]

  lists problems of a contest/category on the judge

Options:
  -j, --judge [codechef|iarcs]
  -c, --contest TEXT            contest code
  --help                        Show this message and exit.
```

### this
```
Usage: termicoder view this [OPTIONS]

  display the termicoder contents in current/passed folder

  if it is a contest folder it displays the list of problems.
  if its a problem folder, displays the problem in a browser.

Options:
  -f, --folder PATH
  --help             Show this message and exit.
```
