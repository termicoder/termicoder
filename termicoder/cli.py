# this file manages the basic cli of termicoder and calls the correct function
import click
import os
from termicoder.utils import display, parse
import termicoder.utils.test as test_module
import termicoder.utils.code as code_module

# Only need to change this on adding new judges if structure is followed
# take care of ',' (comma) while editing this list!
# for default structure visit https://termicoder.github.io
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
@click.option("-f", "--folder", type=click.Path())
def this(folder):
    '''
    display the termicoder contents in current/passed folder
    if it is a contest folder it displays the list of problems
    if a problem folder displays the problem in a browser
    '''
    display.current_dir(folder)

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
def setup(judge, contest, problem,status):
    """
    sets up problem, contests and login.

    if you pass judge and --login/--logout, it logs you in and out of the judge

    if you pass judge (and/or contest/category)
    it downloads all the problems of that contest.

    if you pass a particular problem , with judge (and/or contest/category),
    it sets up that problem all this happens in the current folder.\n
    of contest/category may vary amongst various online judges
    """
    eval(judge).setup(contest, problem,status)


@click.command()
@click.option('-f', '--file', 'code_file',
                type=click.Path(writable=True,readable=False, dir_okay=False),
                help="the filename to code into with preloaded template",
                prompt=True)
@click.option('-et',"--edit_templates", is_flag=True, default=False,
            help="open templates folder")
@click.option('-ed',"--edit_defaults", is_flag=True, default=False,
            help="edit defaults for editors")
def code(code_file,edit_templates,edit_defaults):
    '''
    creates file with template code.\n
    you need to be in a problem directory.
    '''
    if(edit_templates==True):
        code_module.edit_templates()

    elif(edit_defaults==True):
        code_module.edit_defaults()

    code_module.code(code_file)


@click.command()
@click.option('-f', '--file', 'code_file', type=click.File(),
                help="the code file")
@click.option('-es',"--edit_scripts",is_flag=True,default=False)
@click.option('-tl','--timelimit',type=float,help="the max time per testcase")
def test(code_file,edit_scripts,timelimit):
    '''
    test code against the sample testcases.\n
    it (compiles and) runs your program
    and outputs the diff of expected and produced outputs.
    It also outputs time for particular
    '''
    if(edit_scripts==True):
        test_module.edit_scripts()

    judge=parse.get_judge()
    if(not code_file):
        code_file=parse.get_code_file()
    code_file=parse.get_file_name(code_file)
    test_module.test(code_file,timelimit)


@click.command()
@click.option('-f', '--file', 'code_file', type=click.File(),
                help="the code file")
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
    judge=parse.get_judge()
    if(not code_file):
        code_file=parse.get_code_file()
    code_file=parse.get_file_name(code_file)
    eval(judge).submit(code_file)


@click.command()
def debug():
    '''
    launches custom debug interface (in future)
    where you can use testcase generator,
    launch debugger for the particular language
    and visualize the output
    '''
    click.echo('This functionality is not implemented in this version\n'+
    'The command is only kept for compactiblity with future versions\n'+
    'If you want to contribute to its developement visit:\n'+
    'https://termicoder.github.io/')

main.add_command(view)
main.add_command(setup)
main.add_command(code)
main.add_command(test)
main.add_command(submit)
main.add_command(debug)
