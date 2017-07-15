# poor error checking for this module
import click
import os
import sys
import subprocess
import termicoder.utils.display as display
import termicoder.utils.parse as parse
import time

lang_map={
".py":"python",
".c":"c",
".cpp":"cpp",
".cc":"cpp",
".c++":"cpp"
}

interpreted=["python"]

def get_script_folder():
    # though not correct but will work
    if "nt" in os.name:
        return "bat"
    else:
        return "bash"

def get_shell():
    if "nt" in os.name:
        return "cmd.exe"
    else:
        return "bash"

def test(code_file):
    # TODO: check for testcase folder if not found then exit
    # code file will exist; thanks to 'click'
    time_limit = parse.get_time_limit()
    memory_limit = parse.get_memory_limit()

    extension=os.path.splitext(code_file)[1]
    try:
        lang=lang_map[extension]
    except:
        click.echo("the following language extension is not supported:"
                    +extension)
        sys.exit()
    else:

        # retriving the correct bash and batch scripts #######################
        scripts_folder=os.path.join(os.path.dirname(__file__),"scripts")
        os_scripts=os.path.join(scripts_folder,get_script_folder())
        if(lang == "python"):
            ver=click.prompt("please provide python version",
            type=click.Choice([2,3]),default=3)
            lang_folder="py"+str(ver)
        else:
            lang_folder=lang
        lang_folder=os.path.join(os_scripts,lang_folder)
        compile_script=None
        run_script=None
        for s in os.listdir(lang_folder):
            sname=os.path.splitext(s)[0]
            if(sname=="compile"):
                compile_script=os.path.join(lang_folder,s)
            elif(sname=="run"):
                run_script=os.path.join(lang_folder,s)
        ######################################################################

        # using subprocess.call to maintain backward compactiblity with py2
        # if language is compiled
        # call scripts to compile
        #TODO: then print time
        shell_command=get_shell()
        if(lang not in interpreted):
            executable_name=os.path.splitext(code_file)[0]
            compilecall=["bash",compile_script,code_file,executable_name]
            click.echo("compiling...",nl=False)
            start=time.clock()
            a=subprocess.call(compilecall)
            stop=time.clock()
            tdiff=stop-start

            #TODO: print status here instead of done
            click.echo("\t Done",nl=False)
            click.echo("\t compile time: %.4fs\n" % tdiff)

            # if process return a non zero exit code
            if(a):
                sys.exit()

        else:
            executable_name=code_file

        # run on testcases
        #call scripts to output to a file ; then print time
        #script takes arguments as in_filename and out_filename

        testcase_dir="testcases"
        testcase_files=os.listdir(testcase_dir)
        click.echo("running...")
        for testcase_file in testcase_files:
            filename=os.path.splitext(testcase_file)[0]
            file_extension=os.path.splitext(testcase_file)[1]

            #TODO print time and diff
            if(file_extension == ".in"):
                status="AC"
                infile=os.path.join("testcases",testcase_file)
                outfile=os.path.join("testcases",filename+".outx")
                runcall=[get_shell(),run_script,executable_name,infile,outfile]

                click.echo("testcase "+filename,nl=False)
                start=time.clock()
                try:
                    a=subprocess.call(runcall,timeout=time_limit)
                except subprocess.TimeoutExpired:
                    status="TLE"

                stop=time.clock()
                tdiff=stop-start
                click.echo("\t %s"%status,nl=False)
                click.echo("\t Time: %.4fs" % tdiff)


def edit_scripts():
    click.confirm("This will open the scripts folder in file manager\n"+
    "Where you can edit compile and run scripts\n"
    "Do you want to contnue?",default=True,abort=True)
    scripts_folder=os.path.join(os.path.dirname(__file__),"scripts")
    click.launch(scripts_folder)
    sys.exit()
