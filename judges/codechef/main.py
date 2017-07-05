'''
dummy main function
'''
problems=["SANDWICH","UNICOURS","GPD","CHEFBATL"]
from builtins import input
import session
import setup
import console

def dummymain():
    session.load()
    #code=str(input("enter a contest code"))
    #setup.setup_contest(code)
    for pc in problems:
        setup.setup_problem("MAY17",pc)
    

if __name__=="__main__":
    dummymain()
    
    
def main():
    console.log("To be implemented")
