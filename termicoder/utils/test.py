import click
from . import config
from .logging import logger
from .load import get_default_code_name
import subprocess
import sys
from .import yaml
from .import style
import os


# TODO refractor code
def test(code_file, timelimit, live, judge_factory):
    if '.problem.yml' not in os.listdir():
        logger.error("You should be in a problem directory to test")
        return
    else:
        problem = yaml.read('.problem.yml')
        judge = judge_factory.get_judge(problem.judge_name)

    if(code_file is None):
        default_file = get_default_code_name()
        if (not os.path.exists(default_file)):
            default_file = None
        code_file = click.prompt(
            "Please a code file to test",
            default=default_file,
            type=click.Path(readable=True, exists=True, dir_okay=False)
        )

    build_name, extension = code_file.split(".")

    # this envs may be used in build scripts
    os.environ['TERMICODER_EXTENSION'] = extension
    os.environ['TERMICODER_FILE_NAME'] = code_file
    os.environ['TERMICODER_BUILD_NAME'] = build_name

    test_config = config.read('lang/%s/test.yml' % extension)
    if(test_config is None):
        logger.error(
            "No build configurations found for .%s files" % extension
        )
        raise click.Abort

    try:
        build_command = test_config['build']
        run_command = test_config['run']
    except KeyError:
        logger.error("Invalid test.yml")
        raise click.Abort

    # build the file
    # build_commands may be None for interpreted languages
    if build_command is not None:
        if(not isinstance(build_command, list)):
            build_command = [build_command]
        build_command = [
            x.replace(r'{{FILE_NAME}}', code_file) for x in build_command]
        build_command = [
            x.replace(r'{{BUILD_NAME}}', build_name) for x in build_command]
        try:
            logger.info('compiling the file %s', code_file)
            p = subprocess.run(build_command, check=True)
        except subprocess.CalledProcessError:
            logger.error('Compile Time Error!')
            return

    # for testing output with input
    # TODO if no .in files, then run --live
    # maybe  move the checking functionality to problem class
    # helpful for interactive problems
    flag_no_in_file = True
    try:
        testcase_files = os.listdir('testcases')
        assert(os.path.isdir('testcases'))
    except BaseException:
        testcase_files = []

    if live is True:
        testcase_files = ["stdin"]

    for testcase_file in testcase_files:
        if(live or testcase_file.endswith('.in')):
            if(not live and testcase_file.endswith('.in')):
                flag_no_in_file = False
                name = testcase_file.split('.')[0]
                inp_file = click.open_file(
                    os.path.join('testcases', "%s.in" % name))
                inp = inp_file.read()
                inp_file.seek(0)
                try:
                    ans_file = click.open_file(
                        os.path.join('testcases', "%s.ans" % name))
                    ans = ans_file.read()
                    flag_no_ans_file = False
                except BaseException:
                    logger.warn('No ans file found corresponding to testcase %s' % name)
                    logger.warn('output will be logged to %s.out and later '
                                'displayed in pager' % name)
                    ans = None
                    flag_no_ans_file = True
                    pass

                out_file = click.open_file(
                    os.path.join('testcases', "%s.out" % name), 'w')
                testcase = judge.get_testcase(inp=inp, ans=ans, code=name)
            elif live:
                inp_file = sys.stdin
                out_file = sys.stdout

            if(not isinstance(run_command, list)):
                run_command = [run_command]

            logger.debug(run_command)
            run_command = [
                x.replace(r'{{FILE_NAME}}', code_file) for x in run_command]
            run_command = [
                x.replace(r'{{BUILD_NAME}}', build_name) for x in run_command]
            try:
                logger.info('running the code %s on %s' %
                            (build_name, testcase_file))

                if timelimit is None and not live:
                    timelimit = problem.timelimit

                logger.debug(run_command)
                p = subprocess.run(run_command, stdin=inp_file,
                                   timeout=timelimit, check=True,
                                   stdout=out_file, stderr=out_file)
                if not live:
                    out_file.close()
                    out_file = click.open_file(
                        os.path.join('testcases', "%s.out" % name), 'r')
                    out = out_file.read()
                    if(flag_no_ans_file):
                        logger.warn('launching output in pager')
                        click.confirm('continue?', default=True, abort=True)
                        click.echo_via_pager(out)
                        return
                else:
                    return
            except subprocess.TimeoutExpired:
                logger.error('TimeLimitExceeded!')
                return
            except subprocess.CalledProcessError:
                logger.error('RunTimeError!')
                return
            else:
                if(not(live or flag_no_ans_file)):
                    diff = testcase.diff(out)
                    if diff is not None:
                        logger.error('WA')
                        logger.warn('launching diff in pager')
                        click.confirm('continue?', default=True, abort=True)
                        click.echo_via_pager(diff)
                    else:
                        logger.info(style.ac('AC for testcase %s' % name))

    if(flag_no_in_file is True):
        logger.warn('No input files found in current directory')
        click.confirm('run the program live??', default=True, abort=True)
        test(code_file=code_file, timelimit=timelimit, live=True,
             judge_factory=judge_factory)
