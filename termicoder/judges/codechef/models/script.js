//TODO shift to script1.js
mathjax_src = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"

function mathjax_config(){
    MathJax.Hub.Config({
        tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}
    });
}

function load_mathjax(){
    console.log('loading mathjax')
    script = document.createElement('script');
    script.onload = mathjax_config
    script.src = mathjax_src
    document.getElementsByTagName('head')[0].appendChild(script);
}


function start_load() {
    console.log('in start load')
    load_mathjax()
}


window.onload = start_load
