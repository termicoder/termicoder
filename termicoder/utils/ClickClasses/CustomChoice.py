import click


# TODO use this for implementing case insensitive judge options
# along with number based options 1 2 3 4
# along with shortcut options like cc for codechef
# so that user doesnot have to enter the complete name of the judge
class CustomChoice(click.Choice):
    name = 'OJ'
