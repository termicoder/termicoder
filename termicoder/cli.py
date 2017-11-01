# this file manages the basic cli of termicoder and calls the correct function
import click
from termicoder.utils import parse
import termicoder.utils.test as test_module
import termicoder.utils.code as code_module
import termicoder.utils.viewthis as viewthis_module

# Only need to change this on adding new judges if structure is followed
# take care of ',' (comma) while editing this list!
# for default structure visit https://termicoder.github.io
OJs = sorted([
    'iarcs',
    'codechef'
])
###############################################################################

# importing OJ's Modules
for OJ in OJs:
    exec("import termicoder.judges.%s.main as %s" % (OJ, OJ))


@click.group()
def main():
    '''
    view, code & submit problems directly from terminal.
    '''
    pass


# view command has various subcommands
@click.group()
def view():
    '''
    view contests, problems and problem statement
    '''
    pass


@click.command(short_help="display contest list of a judge")
@click.option('-j', '--judge', type=click.Choice(OJs),
              prompt="Please provide a judge("+'|'.join(OJs)+")")
def contests(judge):
    '''
    lists current and upcoming contests on a judge.

    depending on judge it may give a list of categories also
    such as PRACTICE etc.
    '''
    eval(judge).view_contests()


@click.command(short_help="list problems of a contest/category")
@click.option('-j', '--judge', type=click.Choice(OJs),
              prompt="Please provide a judge("+'|'.join(OJs)+")")
@click.option('-c', '--contest', type=click.STRING, help="contest code")
def problems(judge, contest):
    '''
    lists problems of a contest/category on the judge
    '''
    eval(judge).view_problems(contest)


@click.command(short_help="view contents of current folder")
@click.option("-f", "--folder", type=click.Path())
@click.option("-ed", "--edit_defaults", is_flag=True, default=False,
              help="edit default web browser")
def this(folder, edit_defaults):
    '''
    display the termicoder contents in current/passed folder

    \b
    if it is a contest folder it displays the list of problems.
    if its a problem folder, displays the problem in a browser.
    '''
    viewthis_module.view(folder, edit_defaults)


view.add_command(contests)
view.add_command(problems)
view.add_command(this)
###############################################################################


@click.command()
@click.option('-j', '--judge', type=click.Choice(OJs),
              prompt="Please provide a judge("+'|'.join(OJs)+")")
@click.option('-c', '--contest', type=click.STRING, help="contest code")
@click.option('-p', '--problem', type=click.STRING, help="problem code")
@click.option('--login', 'status', flag_value='login')
@click.option('--logout', 'status', flag_value='logout')
def setup(judge, contest, problem, status):
    """
    sets up problem, contests and login.

    1. if you pass judge and --login/--logout,
    it logs you in and out of the judge

    2. if you pass judge and contest/category
    it downloads all the problems of that contest.

    3. if you pass a particular problem, with judge and contest/category,
    it sets up that problem.

    all this happens in the current folder.
    option of contest/category may vary amongst various online judges
    """
    eval(judge).setup(contest, problem, status)


@click.command()
@click.option('-f', '--file', 'code_file',
              type=click.Path(writable=True, readable=False, dir_okay=False),
              help="the filename to code into with preloaded template")
@click.option('-et', "--edit_templates", is_flag=True, default=False,
              help="open templates folder")
@click.option('-ed', "--edit_defaults", is_flag=True, default=False,
              help="edit defaults for editors")
def code(code_file, edit_templates, edit_defaults):
    '''
    creates & open code file with template code.

    you can edit template code and default editors
    using flags -et and -ed respectively
    '''
    if(edit_templates):
        code_module.edit_templates()

    elif(edit_defaults):
        code_module.edit_defaults()

    elif(code_file is None):
        code_file = code_module.get_file_name()

    if(code_file is not None):
        code_module.code(code_file)


@click.command()
@click.option('-f', '--file', 'code_file', type=click.File(),
              help="the code file")
@click.option('-tl', '--timelimit', type=float,
              help="the max time per testcase")
@click.option('-l', '--live', is_flag=True, default=False,
              help="test the code live and don't use testcases")
@click.option('-es', "--edit_scripts", is_flag=True, default=False)
def test(code_file, edit_scripts, timelimit, live):
    '''
    test code against the sample testcases.

    \b
    this command (compiles and) runs passed code file.
    the code is run against all [.in] files in ./testcases folder.
    the output is produced in [.outx] files and checked against [.out] files

    it displays time for each testcase,status
    and diff of expected and produced outputs.
    '''
    if(edit_scripts):
        test_module.edit_scripts()

    if(not code_file):
        code_file = parse.get_code_file()
    code_file = parse.get_file_name(code_file)
    test_module.test(code_file, timelimit, live)


@click.command()
@click.option('-f', '--file', 'code_file', type=click.File(),
              help="the code file")
def submit(code_file):
    '''
    submit a solution.

    you should be in a problem directory to submit

    \b
    script will prompt you to login into the judge(if not already).
    this submits the problem using data in [.problem] file in current directory
    '''
    judge = parse.get_judge()
    if(not code_file):
        code_file = parse.get_code_file()
    code_file = parse.get_file_name(code_file)
    eval(judge).submit(code_file)


@click.command()
def debug():
    '''
    launches custom debug interface (in future)
    where you can use testcase generator,
    launch debugger for the particular language
    and visualize the output
    '''
    click.echo(
        'This functionality is not implemented in this version\n' +
        'The command is only kept for compactiblity with future versions\n' +
        'If you want to contribute to its developement visit:\n' +
        'https://termicoder.github.io/')


main.add_command(view)
main.add_command(setup)
main.add_command(code)
main.add_command(test)
main.add_command(submit)
main.add_command(debug)
