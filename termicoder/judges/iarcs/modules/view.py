import click
import termicoder.utils.display as display
import termicoder.utils.style as style
import termicoder.judges.iarcs.modules.utils.session as session
import termicoder.judges.iarcs.modules.utils.scrape as scrape

def division_line():
    return("+"+"+".join(["-"*3,"-"*10,"-"*25])+"+")

def problems():
    display_strings=[]
    display.normal("requesting problem list from server...")
    if(session.is_logged_in()==True):
        display_strings.append(style.normal(
        "only unsolved problems are being displayed"))
    else:
        display_strings.append(style.normal("you are not logged in\n"+
        "displaying all the problems"))
    # the following line involves a request
    # problems are unsolved ones if logged in
    problems=scrape.get_problem_list()
    display_strings.append(division_line())
    display_strings.append("|"+style.sno("SNo",3)+
                    "|"+style.problem_code("Code",10)+
                    "|"+style.problem_name("Name",25)+"|")
    display_strings.append(division_line())
    for (sno,problem) in zip(range(len(problems)),problems):
        display_strings.append(
                    "|"+style.sno(str(sno+1),3)+
                    "|"+style.problem_code(problem["problem_code"],10)+
                    "|"+style.problem_name(problem["problem_name"],25)+"|")
    display_strings.append(division_line())
    click.echo_via_pager('\n'.join(display_strings))
