# This script extracts problem list from spoj

def extract_problems(link):
    r = session.get(link)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
    rows = soup.find('tbody').find_all('tr')

    problems = []
    # problems is a list of tuples in format(ID, NAME, QUALITY, USERS, IMPLEMENTATION, CONCEPT, PROBLEM_LINK)

    for row in rows:
        quality,implementation,concept = None,None,None
        columns = row.find_all('td')
        ind = columns[1].get_text().strip()
        problem_link = columns[2].find('a')
        if (columns[3].find('span')):
            quality = columns[3].find('span').get_text().strip()
        submissions = columns[4].find('a').get_text()
        accuracy = columns[5].find('a').get_text()
        difficulty = columns[6].find('div').find_all('div')
        if (len(difficulty) > 0 and difficulty[0].find('span')):
            implementation = difficulty[0].find('span').get_text()
        if (len(difficulty) > 1 and difficulty[1].find('span')):
            concept = difficulty[1].find('span').get_text()
        name = problem_link.get_text().strip()
        if (version):
            name = name.encode('utf-8')
        if (ind == '6681'):
            name = "".join(re.findall("[a-zA-Z]+", name))
        problems.append((ind, name, quality, submissions, accuracy, implementation, concept, problem_link.get('href')))
    return problems

