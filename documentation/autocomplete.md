**Method 1:**  
run the following command every time you use terminal  
`eval "$(_TERMICODER_COMPLETE=source termicoder)"`  

**Method 2:**  
put the following command in your .bashrc  
`eval "$(_TERMICODER_COMPLETE=source termicoder)"`  

**Method 3:**  
Method 2 makes bash to load up slowly, so try:  
`eval "$(_TERMICODER_COMPLETE=source termicoder)" > autocomplete.sh`  
and put . path_to_autocompte.sh/autocomplete.sh in your .bashrc  
