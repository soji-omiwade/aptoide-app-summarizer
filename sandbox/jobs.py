from requests import get
from bs4 import BeautifulSoup
from mathematicians import simple_get

def get_me_jobs(job_elems):
    #mjobs=results.find_all("h2", )
    for job_elem in job_elems: 
        title,company,loc=(
            job_elem.find("h2", class_="title", string=lambda text: "Mechanical Engineer" in text)
            , job_elem.find("div",class_="company")
            , job_elem.find("div",class_="location")
        )
        
        if not None in (title, company,loc):
            print("{}|{}|{}".format(title.text.strip(), company.text.strip(),loc.text.strip()))

if __name__ == "__main__":
    a=simple_get("https://www.monster.com/jobs/search/?q=Mechanical-Engineer&where=Texas")
    soup=BeautifulSoup(a,"html.parser")
    results=soup.find(id="ResultsContainer")
    job_elems=results.find_all('section', class_='card-content')
    get_me_jobs(job_elems)
