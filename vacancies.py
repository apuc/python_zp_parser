import requests
import json
from companies import InsertCompany
from tables import Companies, CONNECTION, Vacancies, Categories, Specialities, Category_Speciality_Vacancies
from sqlalchemy import select, insert


def base_func():
    offset = 0
    LIMIT_VACANCIES = 50
    while True:
        index_url = f'https://rostov.zarplata.ru/api/v1/vacancies?geo_id=915&sort=date&offset={offset}&q=&headers_facets=1&limit=50'
        response = requests.get(index_url)
        tree = json.loads(response.text)
        vacancies = tree['vacancies']

        print(offset,'-',offset+LIMIT_VACANCIES)
        
        if(len(vacancies)):
            for vacancy in vacancies:
                result = select(Vacancies).where(Vacancies.id == vacancy['id'])
                is_vacancy = CONNECTION.execute(result).fetchone()
                if(is_vacancy == None):
                    try:
                        result = select(Companies).where(Companies.id == vacancy['publication']['company_id'])
                        is_company = CONNECTION.execute(result).fetchone()
                        if(is_company == None):
                            company_id = vacancy['publication']['company_id']
                            if(company_id == None):
                                continue
                            response = requests.get(f'https://rostov.zarplata.ru/api/v1/companies/{company_id}/')
                            tree = json.loads(response.text)
                            company = tree['companies'][0]
                            InsertCompany(company)
                        insert_vacancy = insert(Vacancies).values(id=vacancy['id'], price=vacancy['salary'], company_id=vacancy['publication']['company_id'], header=vacancy['header'], description=vacancy['description'], payment_type_alias=vacancy['payment_type_alias'])
                        CONNECTION.execute(insert_vacancy)
                    except:
                        print('Error, not enough data')
                        continue
        
                for category in vacancy['rubrics']:
                    result = select(Categories).where(Categories.id == category['id'])
                    is_category = CONNECTION.execute(result).fetchone()
                    if(is_category == None):
                        insert_category = insert(Categories).values(id=category['id'], title = category['title'])
                        CONNECTION.execute(insert_category)
                    for speciality in category['specialities']:
                        result = select(Specialities).where(Specialities.id == speciality['id'])
                        is_speciality = CONNECTION.execute(result).fetchone()
                        if(is_speciality == None):
                            insert_speciality = insert(Specialities).values(id=speciality['id'], title = speciality['title'])
                            CONNECTION.execute(insert_speciality)
                        insert_category_speciality_vacancies = insert(Category_Speciality_Vacancies).values(category_id=category['id'], speciality_id = speciality['id'], vacancy_id=vacancy['id'])
                        CONNECTION.execute(insert_category_speciality_vacancies)
            offset+=LIMIT_VACANCIES
        else:
            print('end')
            break

if __name__ == "__main__":
    base_func()