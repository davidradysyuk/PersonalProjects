#import requests
#from bs4 import BeautifulSoup

#skill =  input('What skill do you want to analyze?')
#URL = f'https://www.upwork.com/search/freelance-jobs/{skill}/'

#page = requests.get(URL)

#soup = BeautifulSoup(page.content, "html.parser")

#results = soup.find("div", class_="visitor-page-container")

#print (results)

import requests
from bs4 import BeautifulSoup

def get_available_jobs(language):
    base_url = f'https://www.upwork.com/o/jobs/browse/skill/{language}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    with requests.Session() as session:
        response = session.get(base_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            job_count_element = soup.find('span', class_='results-total')
            if job_count_element:
                job_count = job_count_element.get_text(strip=True)
                return job_count
            else:
                return "Job count not found."
        else:
            return "Failed to fetch data."

if __name__ == "__main__":
    language_input = input("Enter a language: ")
    job_count = get_available_jobs(language_input)
    print(f"Available jobs for {language_input}: {job_count}")


