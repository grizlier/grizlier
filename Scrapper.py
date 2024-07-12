from bs4 import BeautifulSoup as BS
import requests
import xlsxwriter

workbook = xlsxwriter.Workbook('Вакансии.xlsx')
worksheet = workbook.add_worksheet()

max_pages = 5

row = 0
col = 0

worksheet.write(row, col, 'Сайт, страница')
worksheet.write(row, col+1, 'Вакансия')
worksheet.write(row, col+2, 'Регион')
worksheet.write(row, col+3, 'Зарплата')

row += 1


def scrapping(url, vacancy_option, name_param, region_param, salary_param, worksheet_param, headers = None):
    global row, col

    spisok = {}

    for p in range(max_pages):
        cur_url = f"{url}{p + 1}"

        row += 1

        site_page = worksheet_param + ", " + str(p+1)

        html = requests.get(cur_url, headers=headers).text if headers else requests.get(cur_url).text
        soup = BS(html, 'html.parser')

        vacancies = soup.select(vacancy_option)

        for i, vacancy in enumerate(vacancies, start = len(spisok) + 1):
            spisok[i] = {}

            name = vacancy.select_one(name_param).text.strip()
            try:
                region = vacancy.select_one(region_param).text.strip()
            except AttributeError:
                region = "Регион не указан"
            if "в других городах" in region:
                region = region.replace("в других городах", " ")
                region = region.rstrip()
            try:
                salary = vacancy.select_one(salary_param).text.strip()
            except AttributeError:
                salary = "Договорная"
            spisok[i]["name"] = name
            spisok[i]["region"] = region
            spisok[i]["salary"] = salary

            worksheet.write(row, col, site_page)
            worksheet.write(row, col+1, spisok[i]['name'])
            worksheet.write(row, col+2, spisok[i]['region'])
            worksheet.write(row, col+3, spisok[i]['salary'])
            row += 1
    return row


qyzmet_options = {
    'url': 'https://qyzmet.kz/vacansii?page=',
    'vacancy_option': 'article.job.no-logo',
    'name_param': 'a.job-title',
    'region_param': 'div.job-data.region',
    'salary_param': 'div.job-data.salary',
    'worksheet_param': 'qyzmet',
}

hh_options = {
    'url': 'https://hh.kz/search/vacancy?area=40&search_field=name&search_field=company_name&search_field=description&text=&enable_snippets=false&L_save_area=true&page=',
    'vacancy_option': 'div.vacancy-card--H8LvOiOGPll0jZvYpxIF.font-inter',
    'name_param': 'span.vacancy-name--SYbxrgpHgHedVTkgI_cA.serp-item__title-link.serp-item__title-link_redesign',
    'region_param': 'span[data-qa="vacancy-serp__vacancy-address"]',
    'salary_param': 'span.compensation-text--cCPBXayRjn5GuLFWhGTJ.fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj.separate-line-on-xs--pwAEUI79GJbGDu97czVC',
    'worksheet_param': 'hh',
    'headers': {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
}

olx_options = {
    'url': 'https://www.olx.kz/rabota/?page=',
    'vacancy_option': 'div.jobs-ad-card.css-1qmjf8h',
    'name_param': 'a.css-13gxtrp',
    'region_param': 'span.css-d5w927',
    'salary_param': 'p.css-1jnbm5x',
    'worksheet_param': 'olx',
}

enbek_options = {
    'url': 'https://www.enbek.kz/ru/search/vacancy?except[subsidized]=subsidized&page=',
    'vacancy_option': 'div.item-list',
    'name_param': 'div.title',
    'region_param': 'li.location.d-flex.align-items-center.me-lg-3',
    'salary_param': 'div.price',
    'worksheet_param': 'enbek',
}


scrapping(**qyzmet_options)
row += 1
scrapping(**hh_options)
row += 1
scrapping(**olx_options)
row += 1
scrapping(**enbek_options)

workbook.close()