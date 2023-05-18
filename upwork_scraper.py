import time
from bs4 import BeautifulSoup
from selenium import webdriver


def scrape_freelancers_data():
    URL = "https://www.upwork.com/ab/profiles/search/?category_uid=531770282580668418&page=1&top_rated_plus=yes"
    driver = webdriver.Chrome(executable_path="chromedriver")
    driver.get(URL)
    time.sleep(15)
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    names = soup.find_all('div', {'class': 'identity-name'})    # name
    roles = soup.find_all('p', {'class': 'my-0 freelancer-title'})  # role
    profile_links = soup.find_all('div', {'class': 'd-flex justify-space-between align-items-start'})  # profile_link
    countries = soup.find_all('span', {'class': 'd-inline-block vertical-align-middle'})   # country
    hourly_rates = soup.find_all('div', {'data-qa': 'rate'})  # hourly_rate
    total_earneds = soup.find_all('span', {'data-test': 'earned-amount-formatted'})  # total_earned
    job_success_scores = soup.find_all('span', {'class': 'up-job-success-text'})  # job_success_score
    badges = soup.find_all('span', {'class': 'status-text d-flex top-rated-badge-status'})  # badge
    bios = soup.find_all('div', {'class': 'up-line-clamp-v2 clamped'})  # bio
    company_names = soup.find_all('div', {'class': 'd-flex align-items-center up-btn-link'})  # company_name
    company_earns = soup.find_all('div', {'class': 'ml-10 agency-box-stats'})  # company_earn
    raw_htmls = soup.find_all('div', {'class': 'up-card-section up-card-hover'})  # raw_html
    company_links = soup.find_all(
        'div', {'class': 'cfe-ui-freelancer-tile-agency-box-legacy mt-5 mt-10 agency-box-legacy--link'})

    freelancers_data = []

    for name, role, profile_link, country, hourly_rate, total_earned, job_success_score, badge, bio, company_name, company_earn, raw_html, company_link in zip(names, roles, profile_links, countries, hourly_rates, total_earneds, job_success_scores, badges, bios, company_names, company_earns, raw_htmls, company_links):

        split_data = str(profile_link).split()
        sliced_data = split_data[9:10]
        split_sliced_data = sliced_data[0].split("=")
        final = split_sliced_data[1]
        final = final.replace('"', '')
        joined_final = 'https://www.upwork.com/freelancers/' + final

        split_data = str(company_link).split()
        sliced_data = split_data[5:6]
        split_sliced_data = sliced_data[0].split('=')
        sliced_split_sliced_data = split_sliced_data[1:]
        cleaned_data = sliced_split_sliced_data[0].strip('[]').strip('"')
        company_link_final = 'https://www.upwork.com/agencies/' + cleaned_data

        freelancer_data = {
            "Name": name.text.strip(),
            "Role": role.text.strip(),
            "Profile Link": joined_final,
            "Country": country.text.strip(),
            "Hourly Rate": hourly_rate.text.strip(),
            "Total Earned": total_earned.text.strip(),
            "Job Success Score": job_success_score.text.strip().replace('\n', '').replace('            ', ''),
            "Badge": badge.text.strip(),
            "Bio": bio.text.strip(),
            "Company Name": company_name.text.strip(),
            "Company Earn": company_earn.text.strip(),
            "Raw HTML": raw_html.prettify(),
            "company links": company_link_final
        }
        freelancers_data.append(freelancer_data)

    driver.quit()

    return freelancers_data


data = scrape_freelancers_data()

for freelancer in data:
    print(freelancer)

