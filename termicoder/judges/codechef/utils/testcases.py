from ..models.Testcase import CodechefTestcase as Testcase
from bs4 import BeautifulSoup
from termicoder.utils.logging import logger


# Many corner cases are being handled in extracting testcases
# maybe we can implement our own parser here instead of using
# beautiful soup. Most type of problems should be extracted
def extract(html):
    logger.debug("extract is being called")
    soup = BeautifulSoup(html, "html.parser")
    testcases = []
    pre_tag_elements = soup.find_all('pre')
    try:
        io = _extract_io(pre_tag_elements)
        logger.debug(io)
    except BaseException:
        raise
        logger.error("Extraction of testcase for the problem failed")
        return []

    if(len(pre_tag_elements) >= 1):
        for i in range(len(io[0])):
            inp = io[0][i]
            ans = io[1][i]
            testcases.append(Testcase(inp=inp, ans=ans, code=i))
            logger.debug("inp\n" + inp + "\n\n")
            logger.debug("ans\n" + ans + "\n\n")
        return testcases
    else:
        logger.error("Extraction of testcase for the problem failed")


def _sanitize(io):
    """
    removes ":" "1:" etc if any in front of the io
    """
    # trim begining and ending spaces
    io = io.strip()
    # if Output: Input: etc.
    if(io[0] == ":"):
        io = io[1:]
    # if Output1: Input1: etc
    elif(len(io) > 1 and io[1] == ":"):
        io = io[2:]
    return io.strip()+"\n"


def _extract_io(pre_tag_elements):
    """
    extracts all input and output from pre tags and returns as tuple
    """
    sample_inputs = []
    sample_outputs = []
    for sample_io in pre_tag_elements:
        # finding heading / previous sibling of pre
        sibling = sample_io.previous_sibling
        while(not str(sibling).strip()):
            sibling = sibling.previous_sibling

        # converting sample_io to text
        if sibling is None:
            sibling = sample_io.parent.previous_sibling
            while(not str(sibling).strip()):
                sibling = sibling.previous_sibling
        iotext = str(sample_io.text)

        # standard codechef problems with input and output in same pre tag
        # OR sometimes input just above pre tag and output in pretag
        if(("input" in iotext.lower() or "input" in str(sibling).lower()) and
           "output" in iotext.lower()):
            in_index, out_index = iotext.lower().find(
                "input"), iotext.lower().find("output")
            ki = 1 if (in_index == -1) else 5
            sample_input = _sanitize(iotext[in_index+ki: out_index])
            sample_output = _sanitize(iotext[out_index + 6:])

            if(len(sample_inputs) != len(sample_outputs)):
                sample_inputs = []
                sample_outputs = []
            sample_inputs.append(sample_input)
            sample_outputs.append(sample_output)

        # problem with input only like challenge problems
        # or input and output in separate pre tags
        elif("input" in str(sample_io.text).lower() or
             "input" in str(sibling).lower()):
            in_index = iotext.lower().find("input")
            ki = 1 if (in_index == -1) else 5
            sample_input = _sanitize(iotext[in_index+ki:])
            sample_input = _sanitize(sample_input)
            sample_inputs.append(sample_input)

        # problem with output only like printing 100! etc
        # or input and output in separate pre tags
        elif("output" in str(sample_io.text).lower() or
             "output" in str(sibling).lower()):
            out_index = iotext.lower().find("output")
            ko = 1 if (out_index == -1) else 6
            sample_output = _sanitize(iotext[out_index+ko:])
            sample_output = _sanitize(sample_output)
            sample_outputs.append(sample_output)

    return sample_inputs, sample_outputs
