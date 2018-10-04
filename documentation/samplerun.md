# Sample Run

**NOTE: In some of these commands you may require `sudo` depending on your systems configuration**

1. We start our journey with `termicoder view contests` and `termicoder view problems`  
they give you a list of contests running on a judge and problems of a contest respectively  
e.g. `termicoder view contest -j codechef` will list running and future contests on codechef
`termicoder view problems -j codechef -c cook84` will list all the problems of contest cook84 sorted in descending order of no of submissions

2. Next you have to **setup** problem/contest using `termicoder setup`  
this command creates a directory structure for contests and problems with details such as problem statement, submission info and testcases.  
All the happens in your current directory.  
e.g. `termicoder setup -j codechef -c cook84` will **setup** all the problems from contest cook84 form codechef  
after this command you will have a structure similar to following in your current directory:   
.contest  
COOK84\  
|---PROB1\  
|---|---.problem  
|---|---PROB1.html  
|---|---testcases\  
|---|---|---1.in  
|---|---|---1.out  
|---PROB2\  
.  
.  
.  
instead of names __PROB1__ and __PROB2__  the names would be actual problem codes  
you can view the directory using `ls` on bash or using `DIR` on command prompt  
`.problem` and `.contest` files contain data such as contest code, problem code, judge,timelimit etc. used by termicoder in submitting and testing data  

3. Now you can choose any of the problems to begin  
**Note that most commands such as `view this`, `submit`, `test` work on the basis of your current folder  
so first change your folder to the desired problem folder.**  
on bash you can do this using `cd foldername` for command prompt use `chdir folder name` for the following example we will assume using bash  
say we want to begin with **PROB1**  
so we run  
`cd PROB1`  
`termicoder view this`  
this opens the problem statement (which is saved as html file by termicoder in a problems directory) in your default browser. You can change defaults using `termicoder view this -ed` we recommend use of a commandline browser such as **w3m**/**elinks**  

### NOTE from now we will assume we are in the folder PROB1 untill we say otherwise  

4. Now we have viewed the problem and say we are ready to code.  
**termicoder currently only supports c,c++,java,python**  
so we use the command `termicoder code`.  
this command helps us in coding the solution.  
it puts the template for a language into the given file and opens the problem form editing in the default editor
e.g. `termicoder code -f a.cpp` will create a file a.cpp in current folder loaded with the cpp template and launch the file for editing in your system default for cpp files.   
you can edit default templates using `termicoder code -et`  
you can edit default editor using `termicoder code -ed`  

5. Now say we have coded the solution and we are ready to test this.
for this we use command `termicoder test`  
this command requires us for a code file to test if we don't pass a code file it will automatically look for code files(files with extension .c, .cpp, .py, .java) in the current folder and suggest the latest edited file as default we just have to press enter as in following example.  
after supplying a code file this command (compiles and) runs your code on all testcases and produces diff of reqired and produced outputs  
e.g.  
`termicoder test`  
`Please provide a code file[a.cpp]:`  
after pressing enter, a.cpp is taken as the file, after this termicoder should compile the code(if required).  
Since people use different compilers and systems, compile commannds may vary so instead of hard coding them termicoder uses bash/batch scripts for compiling and running your code  
Some sample scripts have been bundeled for each language but there is quite high chance that they might not work so you need to edit them first. For more details have a look at [CONFIGURE](configure.md).  
To edit scripts run `termicoder test -et`   
After compiling, termicoder runs your code against all `.in` files in testcases folder  
and produces output as a corresponding `.outx` file.   
for example if input is `1.in`, output is produces as `1.outx`  
now the file is compared with corresponding `.out` file which have the expected(correct) output  
i.e. `1.outx` is compared against `1.out`   
after running on all `.in` files it produces status of each case and diff of the outputs.
You can simply add your own testcase by creating a `.in` file and corresponding `.out` file in testcases folder.  
there is no restriction on file name except that they should be same for corresponding `.in` and `.out` files  
The output should match exactly(including spaces) for termicoder to produce AC.  
We do exact check to support accross various judges and problems.  
If it evaluates WA does not always mean that judge will also give WA; You should have a look at diff and .out/.outx files  
test command also has options like timelimit which can be used to set time limit per testcase  
by default it is the timelimit specified in `.problem` file. if not specified it is 3 seconds by default 
ex. `termicoder test -f a.cpp -tl 0.1` makes timelimit 0.1 second per testcase  
to not use testcases files and run the program live use `termicoder test --live`   
it just compiles and runs the program normally taking from stdin and producing to stdout  

6. after testing program and say producing correct output we need to submit our solution  
for that we need to login first.    
to login use `termicoder setup --login -j codechef`  
it prompts you for username and password and logs you in.  
we currently don't support saving username and passwords.  
but we do save cookies and maintain session which help reducing trouble to user,  
though the cookies become invalid soon; the limit depends on judge  
You will have to login again after cookies expire.  
Also you can logout anytime using `termicoder setup --logout -j codechef` which deletes the cookies.  
The cookies may become invalid if you login from some other browser  

7. After we login we can submit a solution using  
`termicoder submit -f a.cpp`  
it gives a confirmation prompt and submits the solution based on data in `.problem` file  
after the judge has evaluated we show you the response.  
Note that if we don't provide option `-f a.cpp`,  
termicoder prompts for a code file similar as the test prompt defaulting to latest code file you edited.  


### Though this run demonstrates most commands of Termicoder, This is by no means exaustive show of termicoder's features. 
