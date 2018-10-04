//TODO correct this
mathjax_src = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"
showdown_src = "https://cdn.rawgit.com/showdownjs/showdown/1.8.6/dist/showdown.min.js"

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

function showdown_config(){
    var conv = new showdown.Converter();
    var txt = document.body.innerHTML;
    console.log(txt);
    document.body.innerHTML = conv.makeHtml(txt);
    load_mathjax()
}

function load_showdown() {
    console.log('loading showdown')
    script = document.createElement('script');
    script.onload = showdown_config
    script.src = showdown_src
    document.getElementsByTagName('head')[0].appendChild(script);
}

function start_load() {
    console.log('in start load')
    load_showdown();
}


window.onload = function() {start_load()}();
