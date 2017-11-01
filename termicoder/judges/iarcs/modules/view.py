import click
import termicoder.utils.style as style
import termicoder.judges.iarcs.modules.utils.session as session
import termicoder.judges.iarcs.modules.utils.scrape as scrape


def division_line():
    return("+"+"+".join(["-"*3, "-"*10, "-"*25])+"+")


def problems():
    display_strings = []
    click.echo("requesting problem list from server...")
    if(session.is_logged_in()):
        display_strings.append(style.normal(
            "You are logged in\n" +
            "Only UNSOLVED problems are being displayed"))
    else:
        display_strings.append(style.normal("you are NOT logged in\n" +
                                            "displaying ALL the problems"))
    # the following line involves a request
    # problems are unsolved ones if logged in
    problems = scrape.get_problem_list()
    click.echo("Done")
    display_strings.append(division_line())
    display_strings.append("|"+style.sno("SNo", 3) +
                           "|"+style.problem_code("Code", 10) +
                           "|"+style.unsolved("Name", 25)+"|")
    display_strings.append(division_line())
    for (sno, problem) in zip(range(len(problems)), problems):
        display_strings.append(
                    "|"+style.sno(str(sno+1), 3) +
                    "|"+style.problem_code(problem["problem_code"], 10) +
                    "|"+style.unsolved(problem["problem_name"], 25)+"|")
    display_strings.append(division_line())
    click.echo_via_pager('\n'.join(display_strings))
