from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver
# jobs = extract_wwr_jobs("python")
# print(jobs)


def get_page_count(keyword):
    driver = webdriver.Chrome()
    base_url = "http://kr.indeed.com/jobs?q="
    driver.get(f"{base_url}{keyword}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    pagination = soup.find("nav", attrs={"aria-label": "pagination"})
    if pagination == None:
        return 1
    pages = pagination.find_all('div', recursive=False)
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    for page in range(pages):
        results = []
        driver = webdriver.Chrome()
        base_url = "http://kr.indeed.com/jobs?q="
        driver.get(f"{base_url}{keyword}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultList")
        jobs = job_list.find_all('li', recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mozaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")

                job_data = {
                    "link": f"http://kr.indeed.com{link}",
                    "company": company.string,
                    "location": location.string,
                    "position": title,
                }
                results.append(job_data)
        while (True):
            pass
