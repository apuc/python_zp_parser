import requests
import json
from tables import Company_rubric, Companies, Rubrics, CONNECTION
from sqlalchemy import select, insert



def InsertCompany(company):
    result = select(Companies).where(Companies.id == company['id'])
    is_company = CONNECTION.execute(result).fetchone()
    if(is_company == None):
        try:
            try:
                number = company['contacts'][0]['phones'][0]['number']
            except:
                number = None

            try:
                formatted_number = company['contacts'][0]['phones'][0]['formatted']
            except:
                formatted_number = None

            insert_company = insert(Companies).values(id=company['id'], email=company['email'], title=company['title'], official_title=company['official_title'], description=company['description'], early_career=company['early_career'], number=number, formatted_number=formatted_number)
            CONNECTION.execute(insert_company)

            for rubric in company['rubrics']:
                result = select(Rubrics).where(Rubrics.id == rubric['id'])
                is_rubric = CONNECTION.execute(result).fetchone()
                if(is_rubric == None):
                    insert_rubric = insert(Rubrics).values(id=rubric['id'], title = rubric['title'])
                    CONNECTION.execute(insert_rubric)
                insert_company_rubric = insert(Company_rubric).values(company_id=company['id'], rubric_id = rubric['id'])
                CONNECTION.execute(insert_company_rubric)
                
        except:
            print('Error, not enough data')


def base_func():
    offset = 0
    LIMIT_COMPANIES = 50
    while True:
        index_url = f'https://rostov.zarplata.ru/api/v1/companies?geo_id=915&limit={LIMIT_COMPANIES}&offset={offset}&rubric_filter_mode=new'
        response = requests.get(index_url)
        tree = json.loads(response.text)
        companies = tree['companies']

        print(offset, '-', offset + LIMIT_COMPANIES)
        
        if(len(companies)):
            for company in companies:
                InsertCompany(company)
            offset += LIMIT_COMPANIES
        else:
            print('end')
            break


if __name__ == "__main__":
    base_func()