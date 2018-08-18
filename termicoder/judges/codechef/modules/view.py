import click
import os
import json
import termicoder.utils.display as display
import termicoder.utils.style as style
import termicoder.judges.codechef.modules.utils.session as session
import termicoder.judges.codechef.modules.utils.scrape as scrape
import termicoder.judges.codechef.modules.utils.date as date_utility

normal_problem_types = ["3", "0"]


def problem_divison_line():
    return("+"+"+".join(["-"*3, "-"*10, "-"*25, "-"*7])+"+")


def contest_divison_line1():
    return("+"+"+".join(["-"*3, "-"*10, "-"*25, "-"*10, "-"*10])+"+")


def contest_divison_line2():
    return("+"+"+".join(["-"*3, "-"*10, "-"*25])+"+")


def problems(contest):
    contest = contest.upper()
    display_strings = []

    if contest == "PRACTICE":
        try:
            catagory_list_path = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), "catagories.json")
            catagory_file = open(catagory_list_path)
            catagory_list = json.load(catagory_file)["catagorylist"]
        except BaseException:
            display.error("INTERNAL ERROR:catagorylist for codechef not found")
            raise click.Abort
        chosen_catagory = click.prompt(
            "Please choose a catagory"+"(" + "|".join(catagory_list) + ")",
            type=click.Choice(catagory_list))
        click.echo("requesting problem list from server...")
        contest_data = scrape.get_practice_problems(chosen_catagory,
                                                    abort=True)
    else:
        click.echo("requesting problem list from server...")
        # the following statement returns data of the contest
        contest_data = scrape.get_contest(contest, abort=True)

    click.echo("Done")

    if(contest_data["user"]["username"]):
        display_strings.append(style.normal(
            "You are logged in.\nOnly UNSOLVED problems are being displayed"))
    else:
        display_strings.append(style.normal("You are NOT logged in\n" +
                                            "displaying ALL the problems"))

    display_strings.append(style.normal("\nContest: ") +
                           style.contest_code(contest_data["code"])+" " +
                           style.contest_name("("+contest_data["name"]+")"))
    if(contest_data["rank_and_score"] and contest_data["user"]["username"]):
        display_strings.append(
            style.normal(
                "Rank: " +
                contest_data["rank_and_score"]["rank"] +
                "\t" +
                "Score: " +
                contest_data["rank_and_score"]["score"]))

    display_strings.append(problem_divison_line())
    display_strings.append("|"+style.sno("SNo", 3) +
                           "|"+style.problem_code("Code", 10) +
                           "|"+style.unsolved("Name", 25) +
                           "|"+style.submissions("Submissions", 7)+"|")
    display_strings.append(problem_divison_line())
    problems = []
    for i in contest_data["problems"]:
        if(i not in contest_data["problemsstats"]["solved"] or
           contest_data["problems"][i]["type"] not in normal_problem_types or
           i in contest_data["problemsstats"]["partially_solved"]):
            problems.append(contest_data["problems"][i])
    problems.sort(key=lambda p: int(p["successful_submissions"]), reverse=True)

    for (sno, problem) in zip(range(len(problems)), problems):
        name_style = style.unsolved
        if(contest_data["problems"][problem["code"]]["type"] not in normal_problem_types):
            name_style = style.challenge
        elif(problem["code"] in contest_data["problemsstats"]["partially_solved"]):
            name_style = style.partially_solved
        elif(problem["code"] in contest_data["problemsstats"]["attempted"]):
            name_style = style.incorrect
        problem_string = "|".join(["",
                                   style.sno(str(sno+1), 3),
                                   style.problem_code(problem["code"], 10),
                                   name_style(problem["name"], 25),
                                   style.submissions(
                                       problem["successful_submissions"], 7),
                                   ""])
        
        try:
            if problem["category_name"] == "unscored":
                problem_string += style.incorrect("unscored")
        except KeyError:
            pass
            display_strings.append(problem_string)

    display_strings.append(problem_divison_line())
    click.echo_via_pager('\n'.join(display_strings))


def contests():
    click.echo("requesting contest list from server...")
    contest_list = scrape.get_contest_list()
    click.echo("Done")
    # sort contests
    contest_list["contests"].sort(key=lambda p: int(p["end_date"]))
    display_strings = []
    running_future_contests = []
    display_strings.append("running and future contests on codechef:")
    display_strings.append(contest_divison_line1())
    display_strings.append("|"+style.sno("SNo", 3) +
                           "|"+style.contest_code("Code", 10) +
                           "|"+style.unsolved("Name", 25) +
                           "|"+style.time("Start", 10) +
                           "|"+style.time("End", 10)+"|")
    display_strings.append(contest_divison_line1())
    for sno, contest in zip(
            range(len(contest_list["contests"])),
            contest_list["contests"]):
        sdate, stime = date_utility.get_date_time(contest["start_date"])
        edate, etime = date_utility.get_date_time(contest["end_date"])

        # adding contest line
        running_future_contests.append(contest["code"])
        display_strings.append("|"+style.sno(str(sno+1), 3) +
                               "|"+style.contest_code(contest["code"], 10) +
                               "|"+style.contest_name(contest["name"], 25) +
                               "|"+style.time(sdate, 10) +
                               "|"+style.time(edate, 10)+"|")

        # adding time line
        display_strings.append("|"+style.sno(" ", 3) +
                               "|"+style.contest_code(" ", 10) +
                               "|"+style.contest_name(" ", 25) +
                               "|"+style.time(stime, 10) +
                               "|"+style.time(etime, 10)+"|")
        display_strings.append(contest_divison_line1())

    display_strings.append('')
    if(contest_list["others"] is not None):
        others = [other for other in contest_list["others"]
                  if other["code"] not in running_future_contests]
        display_strings.append(
            "codechef is also accepting solutions for following:")
        display_strings.append(contest_divison_line2())
        for sno, contest in zip(
                range(
                    len(running_future_contests),
                    len(running_future_contests) + len(others)),
                others):
            display_strings.append("|".join(
                                       ["",
                                       style.sno(str(sno+1), 3),
                                       style.contest_code(contest["code"], 10),
                                       style.contest_name(contest["name"], 25),
                                       ""])
                                   )
        display_strings.append(contest_divison_line2())
    else:
        # if not logged in
        if(not session.is_logged_in(ensure=True)):
            display_strings.extend(
                ["You are not logged in",
                 "There may be some more contests for which",
                 "codechef requires your login to view"])

    click.echo_via_pager('\n'.join(display_strings))
    # display_strings.append("Following contests are running on codechef")
    # display_strings.append("Following contests will be hosted on codechef")
