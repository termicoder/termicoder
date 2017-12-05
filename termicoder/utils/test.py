# FIXME: poor error checking for this module
import click
import os
import sys
import subprocess
import signal
import filecmp
import termicoder.utils.display as display
import termicoder.utils.parse as parse
import termicoder.utils.style as style
import time
diff_strings = [
    '''
Help:
shows first 10 different lines along with line no for each testcase
newlines are shown as \\n
spaces are shown as _''']

lang_map = {
    ".py": "python",
    ".c": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".c++": "cpp",
    ".java": "java"
}

interpreted = ["python"]


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


def is_same(ansfile, outfile):
    a = False
    try:
        a = filecmp.cmp(ansfile, outfile)
    except BaseException:
        display.error("error in infile/outfile")
    return a


def diff(ansfile, outfile):
    pad = style.pad
    a = []
    error = False
    try:
        s1 = open(ansfile, "r").readlines()
        s2 = open(outfile, "r").readlines()
    except BaseException:
        error = True

    if(not error):
        lines = min(len(s1), len(s2))
        lno_pad = max(len(str(lines)), 3)
    else:
        lines = 0
        lno_pad = 3
    a.append('|' + pad("lno", lno_pad) +
             '|' + pad(ansfile, 25) + '|'+pad(outfile, 25)+'|')
    a.append('+' + '-'*lno_pad +
             '+' + '-'*25 + '+' + '-'*25+'+')

    for i in range(lines):
        line1 = s1[i]
        line2 = s2[i]
        if(line1 != line2):
            line1 = line1.replace(' ', '_')
            line1 = line1.replace('\n', '\\n')

            line2 = line2.replace(' ', '_')
            line2 = line2.replace('\n', '\\n')

            sno = str(i+1)
            a.append('|' + pad(sno, lno_pad) +
                     '|' + pad(line1, 25) + '|'+pad(line2, 25)+'|')

            if(len(a) >= 12):
                break

    if(error):
        a.append("error in opening files")
    return '\n'.join(a)


def test(code_file, time_limit, live):
    # TODO: check for testcase folder if not found then exit
    # TODO: check if the answer file exists
    # code file will exist; thanks to 'click'
    if(time_limit is None):
        time_limit = parse.get_time_limit()

    extension = os.path.splitext(code_file)[1]
    try:
        lang = lang_map[extension]
    except BaseException:
        click.echo("the following language extension is not supported:"
                   + extension)
        sys.exit()
    else:

        # retriving the correct bash and batch scripts #######################
        scripts_folder = os.path.join(os.path.dirname(__file__), "scripts")
        os_scripts = os.path.join(scripts_folder, get_script_folder())
        lang_folder = lang
        lang_folder = os.path.join(os_scripts, lang_folder)
        compile_script = None
        run_script = None
        for s in os.listdir(lang_folder):
            sname = os.path.splitext(s)[0]
            if(sname == "compile"):
                compile_script = os.path.join(lang_folder, s)
            elif(sname == "run"):
                run_script = os.path.join(lang_folder, s)
        ######################################################################

        # using subprocess.call to maintain backward compactiblity with py2
        # if language is compiled
        # call scripts to compile
        # TODO: then print time
        shell_command = get_shell()
        if(lang not in interpreted):
            executable_name = os.path.splitext(code_file)[0]
            compilecall = [shell_command, compile_script,
                           code_file, executable_name]
            click.echo("compiling...", nl=False)
            start = time.time()
            a = subprocess.call(compilecall)
            stop = time.time()
            tdiff = stop-start

            # if process return a non zero exit code
            if(a):
                click.echo(style.error("\t COMPILATION ERROR"), nl=False)
                click.echo("\t compile time: %.4fs\n" % tdiff)
                sys.exit()
            # TODO: print status here instead of done
            click.echo("\t Done", nl=False)
            click.echo("\t compile time: %.4fs\n" % tdiff)

        else:
            executable_name = code_file

        if(live):
            runcall = [shell_command, run_script, executable_name]
            click.echo("The program is now running:")
            a = subprocess.call(runcall)
            click.echo(
                "\nTermicoder:\nthe process exited with status code " +
                str(a) +
                "\none \\n was added after your code's output by Termicoder")
        else:
            # run on testcases
            # call scripts to output to a file ; then print time
            # script takes arguments as in_filename and out_filename
            global diff_strings

            testcase_dir = "testcases"
            testcase_files = sorted(os.listdir(testcase_dir))
            click.echo("running...")
            for testcase_file in testcase_files:
                filename = os.path.splitext(testcase_file)[0]
                file_extension = os.path.splitext(testcase_file)[1]

                if(file_extension == ".in"):
                    status = None
                    infile = os.path.join("testcases", testcase_file)
                    outfile = os.path.join("testcases", filename+".outx")
                    stdin = open(infile, "r")
                    stdout = open(outfile, "w")
                    runcall = [shell_command, run_script, executable_name]

                    # TODO: use a better function then time.clock()
                    start = time.time()
                    try:
                        a = subprocess.Popen(
                            runcall,
                            stdin=stdin, stdout=stdout,
                            preexec_fn=os.setsid)
                        a.wait(timeout=time_limit)
                    except subprocess.TimeoutExpired:
                        status = style.error("TLE")
                    except BaseException:
                        click.echo("")
                        status = "Internal Error"  #some other error!! in this
                    return_code=a.poll()
                    if(return_code==None): #process not terminated
                        status = style.error("TLE")
                        os.killpg(os.getpgid(a.pid), signal.SIGTERM) #kills all
                    elif(return_code!=0):  # runtime error
                        status = style.error("RTE")

                    stop = time.time()
                    tdiff = stop-start

                    if(status is None):
                        # check output and append create diff strings
                        ansfile = os.path.join("testcases", filename+".out")
                        if(is_same(ansfile, outfile)):
                            status = style.correct("AC")
                        else:
                            status = style.error("WA")
                            diff_strings.append("\nTestcase "+filename+"\n")
                            diff_strings.append(diff(ansfile, outfile))

                    click.echo("testcase "+filename, nl=False)
                    click.echo("\t %s" % status, nl=False)
                    click.echo("\t Time: %.4fs" % tdiff)

            if(len(diff_strings) > 1):
                click.confirm(
                    "There were some WA's\n" +
                    "Do you want to view the diff page?",
                    default=True,
                    abort=True)
                click.echo_via_pager('\n'.join(diff_strings))


def edit_scripts():
    click.confirm("This will open the scripts folder in file manager\n" +
                  "Where you can edit compile and run scripts\n"
                  "Do you want to contnue?", default=True, abort=True)
    scripts_folder = os.path.join(os.path.dirname(__file__), "scripts")
    click.launch(scripts_folder)
    sys.exit()
