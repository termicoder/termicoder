import click
import termicoder.utils.color as color
style_types=["error",
            "normal",
            "command",
            "problem_code",
            "contest_code",
            "problem_name",
            "contest_name",
            "url",
            "sno"]

# defining all the style_types functions in this loop
# figure a better way out
for style in style_types:
    exec(
    "def "+(style)+"(string,l=None):"+
    '''
    if(l):
        string=pad(string,l)
    return click.style(string,
                fg=color.'''+style+'''_fg,
                bg=color.'''+style+'''_bg,
                bold=color.'''+style+'''_bold)
    ''')


def pad(string,length):
    if(len(string)<=length):
        return string+((" ")*(length-len(string)))
    else:
        return string[:-2]+".."
