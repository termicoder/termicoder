import click
import termicoder.utils.display as display
import termicoder.utils.style as style
import termicoder.judges.codechef.modules.utils.session as session
import termicoder.judges.codechef.modules.utils.scrape as scrape

def division_line():
    return("+"+"+".join(["-"*3,"-"*10,"-"*25,"-"*7])+"+")

def problems(contest):
    contest=contest.upper()
    display_strings=[]
    click.echo("requesting problem list from server...")

    #the following statement returns data of the contest
    contest_data=scrape.get_contest(contest,abort=True)
    click.echo("Done")

    if(contest_data["user"]["username"]):
        display_strings.append(style.normal(
        "You are logged in.\nOnly UNSOLVED problems are being displayed"))
    else:
        display_strings.append(style.normal("You are NOT logged in\n"+
        "displaying ALL the problems"))

    display_strings.append(style.normal("\nContest: ")+
    style.contest_code(contest_data["code"])+" "+
    style.contest_name("("+contest_data["name"]+")"))
    #print(contest_data)
    if(contest_data["rank_and_score"] and contest_data["user"]["username"]):
        display_strings.append(style.normal("Rank: "+
        contest_data["rank_and_score"]["rank"]+"\t"+
        "Score: "+contest_data["rank_and_score"]["score"]))

    display_strings.append(division_line())
    display_strings.append("|"+style.sno("SNo",3)+
                    "|"+style.problem_code("Code",10)+
                    "|"+style.unsolved("Name",25)+
                    "|"+style.submissions("Submissions",7)+"|")
    display_strings.append(division_line())
    problems=[]
    for i in contest_data["problems"]:
        if(i not in contest_data["problemsstats"]["solved"] or
        contest_data["problems"][i]["type"]!="3" or
        i in contest_data["problemsstats"]["partially_solved"]):
            problems.append(contest_data["problems"][i])
    problems.sort(key=lambda p: int(p["successful_submissions"]),reverse=True)

    for (sno,problem) in zip(range(len(problems)),problems):
        name_style=style.unsolved
        if(contest_data["problems"][problem["code"]]["type"]!="3"):
            name_style=style.challenge
        elif(problem["code"] in contest_data["problemsstats"]["partially_solved"]):
            name_style=style.partially_solved
        elif(problem["code"] in contest_data["problemsstats"]["attempted"]):
            name_style=style.incorrect

        display_strings.append(
                "|"+style.sno(str(sno+1),3)+
                "|"+style.problem_code(problem["code"],10)+
                "|"+name_style(problem["name"],25)+
                "|"+style.submissions(problem["successful_submissions"],7)+"|")
    display_strings.append(division_line())
    click.echo_via_pager('\n'.join(display_strings))


def contests():
    print("contests not implemented yet")
