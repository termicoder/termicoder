click.File() has a different `__str__` function,
so don't use default parameter for it in case of commands,
also be careful while taking it as input actually we may only require its name
use click.File().name attrbute , finally for help see parse.codefile function

use click.echo() to print to files also replace all occurences of print
also rem to remove the extra newline at the end in case of testcases

