"""
this module creates the required files of a contest/problem including
json data of contest(.contest file), json data of problem(.problem file) 
html problem statements and testcases

for trial run run this as python3 setup.py
"""
import scrape
import os
import json

def setup_problem(contest_code,problem_code):
    problem_path=os.path.join(".",contest_code,problem_code)
      
    try:
        os.mkdir(problem_path)
    except:
        pass
    
    problem=scrape.get_problem(contest_code,problem_code)
    
    if not problem["error"]:
        problem_html=problem.pop("body") 
        sampleio=problem.pop("sampleio")
        # html problem statement
        if not problem["error"]:
            problem_html_file=os.path.join(problem_path,problem_code+".html")
            f2=open(problem_html_file,"w")
            print(problem_html,file=f2)

        # sampleio files
        if(sampleio["error"]==""):
            testcases_path=os.path.join(problem_path,"testcases")
            try:
                os.mkdir(testcases_path)
            except:
                pass
            for i in range(len(sampleio["inputs"])):
                input_file=os.path.join(testcases_path,str(i+1)+".in")
                ifile=open(input_file,"w")
                print(sampleio["inputs"][i],file=ifile)
            for o in range(len(sampleio["outputs"])):
                output_file=os.path.join(testcases_path,str(o+1)+".out")
                ofile=open(output_file,"w")
                print(sampleio["outputs"][o],file=ofile)
                
    # the problem data
    problem_setup_file=os.path.join(problem_path,".problem")
    f1=open(problem_setup_file,"w")
    print(json.dumps(problem,indent=2,sort_keys=True),file=f1)

    
def setup_contest(contest_code):
    contest_path=os.path.join(".",contest_code)
    try:
        os.mkdir(contest_path)
    except:
        pass
    contest_setup_file=os.path.join(contest_path,".contest")
    f=open(contest_setup_file,"w")
    contest=scrape.get_contest(contest_code)
    del contest["rules"]
    print(json.dumps(contest,indent=2), file=f)
    
    # setup all problems for the contests
    for problem_code in contest["problems"]:
        setup_problem(contest_code,problem_code)
        
if __name__ == "__main__":
    # trial setup of a contest
    setup_contest("JUNE17")
