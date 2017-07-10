# this file manages the basic cli of termicoder and calls the correct function
import click
import os
from termicoder.utils import display, test

# Only need to change this on adding new judges if structure is followed
OJs = [
    'iarcs',
    'codechef'
]
OJs.sort()
###############################################################################

for OJ in OJs:
    exec("import termicoder.judges.%s.main as %s" % (OJ, OJ))


@click.group()
def main():
    '''
    view, code, submit problems directly from terminal.
    '''
    pass


# view command has various subcommands
@click.group()
def view():
    '''
    view contests, problems and problem statement
    '''
    pass


@click.command()
@click.option('-j', '--judge', type=click.Choice(OJs),
              prompt="Please provide a judge("+'|'.join(OJs)+")")
def contests(judge):
    '''
    lists contests/categories running on a judge
    '''
    eval(judge).view_contests()


@click.command()
@click.option('-j', '--judge', type=click.Choice(OJs),
              prompt="Please provide a judge("+'|'.join(OJs)+")")
@click.option('-c', '--contest', type=click.STRING, help="contest code")
def problems(judge, contest):
    '''
    lists problems of a contest/category on the judge
    '''
    eval(judge).view_problems(contest)


@click.command()
@click.option("-r","--recursive",is_flag=True,default=False,
              help="recursive display in current folder upto 1 level")
@click.option("-f", "--folder", type=click.Path())
def this(recursive, folder):
    '''
    display the termicoder contents in current/passed folder
    if it is a contest folder it displays the list of problems
    if a problem folder displays the problem in a browser
    '''
    cwd = os.getcwd()
    display.current_dir(cwd,recursive,folder)

view.add_command(contests)
view.add_command(problems)
view.add_command(this)
#######################################################


@click.command()
@click.option('-j', '--judge', type=click.Choice(OJs))
@click.option('-c', '--contest', type=click.STRING, help="contest code")
@click.option('-p', '--problem', type=click.STRING, help="problem code")
@click.option('--login', 'status', flag_value='login')
@click.option('--logout', 'status', flag_value='logout')
def setup(status, judge, contest, problem):
    """
    prepares directories for termicoder to work.

    if you pass judge and --login/--logout, it logs you in and out of the judge

    if you pass judge (and/or contest/category)
    it downloads all the problems of that contest.

    if you pass a particular problem , with judge (and/or contest/category),
    it sets up that problem all this happens in the current folder.\n
    of contest/category may vary amongst various online judges
    """
    click.echo('setup not implemented yet')
    click.echo('params\n status- %s' % status)
    click.echo('params\n judge-%s' % judge)
    click.echo('params\n contest-%s' % contest)
    click.echo('params\n problem-%s' % problem)


@click.command()
@click.option('-f', '--file', 'code_file', type=click.File())
def code(code_file):
    '''
    creates file with template code.\n
    you need to be in a problem directory.
    '''
    click.echo('code not implemented yet')
    click.echo('params\n code_file-%s' % code_file)


@click.command()
@click.option('-f', '--file', 'code_file', type=click.File())
def test(code_file):
    '''
    test code against the sample testcases.\n
    it (compiles and) runs your program\n
    and outputs the diff of expected and produced output
    '''
    click.echo('test not implemented yet')
    click.echo('params\n code_file-%s' % code_file)


@click.command()
@click.option('-f', '--file', 'code_file', type=click.File())
def submit(code_file):
    '''
    submit a solution.

    you should be in a problem directory to submit\n
    script will prompt you to login into the judge (if not already logged in)\n
    this submits the problem using .problem file in current directory(if exists)
    or the headers in the code file.\n
    the settings of headers in code file dominate if different and valid,
    however if invalid, than the other one is tried
    '''
    click.echo('submit not implemented yet')
    click.echo('params\n code_file- %s' % code_file)


@click.command()
def debug():
    '''
    launchs the debuger
    '''
    click.echo('this functionality is not availible in this version'+
    'this option is only kept for avoiding hastles in future versions')

main.add_command(view)
main.add_command(setup)
main.add_command(code)
main.add_command(test)
main.add_command(submit)
main.add_command(debug)
