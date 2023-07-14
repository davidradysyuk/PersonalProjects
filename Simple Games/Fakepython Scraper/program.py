import requests
from bs4 import BeautifulSoup

position = input('What role would you like to apply for? ')
jobz = ['python', 'manager', 'engineer', 'executive', 'officer', 'designer', 'scientist', 'Interpreter', 'Architect',
        'Meteorologist', 'teacher', 'journalist', 'Surgeon', 'Nurse', 'assistant', 'Programmer', 'Producer']
while position not in jobz:
    position = input('That is not a valid job title. Please enter a new one. ')

URL = 'https://realpython.github.io/fake-jobs/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id='ResultsContainer')

job_elements = results.find_all("div", class_="card-content")

manager_jobs = results.find_all("h2", string=lambda text: position in text.lower())

manager_jobs_elements = [h2_element.parent.parent.parent for h2_element in manager_jobs]

for job_element in manager_jobs_elements:
    title_element = job_element.find('h2', class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    link_url = job_element.find_all("a")[1]["href"]
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print(f"apply here: {link_url}")
    print()
