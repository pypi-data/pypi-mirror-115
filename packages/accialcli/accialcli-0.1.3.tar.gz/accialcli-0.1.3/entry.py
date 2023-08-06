import click
import requests
import json
from datetime import datetime
import datetime as datet
from datetime import date

__host__ = 'https://dev.orca.accialcapital.com/api/integration/'
token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk4QkFBQThDNjZFQTY5NTkiLCJrdHkiOiJSU0EifQ.eyJQYXJ0bmVySWQiOiIyMDZERjNERC05Qjc1LTRDNjAtOTFGNy1ERjQ1MzE4NUEzN0YiLCJleHAiOjE2MzQzMDA4OTgsImlhdCI6MTYwMjc2NDg5OCwianRpIjoiYjA1NGFhMDYtZGUzZC00MzcxLTlmZTYtZmQ4NTZjZjVhODlhIiwicm9sZSI6IlBhcnRuZXIifQ.UVKkfwED6DeAB_8Dx72nLRfZSQrms-2IJXYYYDJBbuJEAPphOsJdC5qM9Kp4RzzLIt5PIhet34nu3gyoll-Xylyor0DhW-g0UE1H_g7_ok8hKwU5ZkJ3Y-3vZnJz0GWKhSMPbts0Mfqxbdlh5gSMacj45vV1MHxtLnC9cULPLBe4ojZ7BDnpJDdia1zGZ6J2a_yG9wNTh8K4y8dDHUktLzH8LWdLOo_ROVYlE5ki58pxF7qQF2KIOGbnTWTB3zBLOgUGg8f2yzt5cMUaxr2Pu_i8aeeypNS7KLoVUTIHIxUYl0cKi6Wkrx9Onc-JdPDF_bo6l60JH9pvqiFNlgPKCg'
__my_headers__ = {'Authorization' : 'Bearer '+  token}
__aplicationdate__ = None

##----DATETIME----###

def tomorrow(paymentDate):
    paymentDate = datetime.fromisoformat(paymentDate)
    paymentDate= paymentDate+ datet.timedelta(days = 1)
    return paymentDate.strftime("%Y-%m-%d")

def validate_date(ctx, param, value):
    if value <= date.today().strftime("%Y-%m-%d"):
        global __aplicationdate__
        __aplicationdate__=  value
        return value
    else:
        raise click.BadParameter("Date invalid, the date must be less or equal than today")
def validate_date_disbursement (ctx, param, value):
    if __aplicationdate__ <= value and value <= date.today().strftime("%Y-%m-%d"):
        return value
    else:
        raise click.BadParameter("The disbursement date must be greater or equal than application date and less or equal than today")

def afterMonths(ourdate , num):
    today =date.today()
    year = int(format(today.year))
    isleapyear = year%4 == 0 and ( year%100!= 0 or year % 400 ==0)
    february = 29 if  isleapyear else 28
    months_year = [31 ,february  ,31, 30 ,31 ,30, 31 ,30 ,30, 31 ,30 ,31]
    for i in range(num):
        date_time_obj = datetime.fromisoformat(ourdate)
        index = int(format(date_time_obj.month)) -1
        month_day = months_year[index]
        datee= date_time_obj+ datet.timedelta(days = month_day)
        date_time = datee.strftime("%Y-%m-%d")
        ourdate = date_time
    return date_time
##-------

def searchId(endpoint, uid , queryname):
    url_format = __host__ +endpoint
    query_params = {
        queryname : uid
    }
    response = requests.get(url_format, params=query_params, headers=__my_headers__)
    click.echo(response.json())

def chooseId(endpoint, type):
    url_items = __host__ + endpoint
    items = requests.get(url_items, headers=__my_headers__)
    items = items.json()
    items_names = list(map(lambda x: x['name'], items))
    choice = click.prompt(
        "\nPlease, choose your "+type+":\n",
        type=click.Choice(items_names),
        show_default=True,
    )
    countryId = list(filter(lambda x: x['name'] == choice, items))
    return countryId[0]['id']

def createBorrower(id):
    countryId = chooseId('tables/countries', 'country')
    educationTypeId = chooseId('tables/educationtypes', 'education type')

    url_format = __host__ +'borrowers'
    id = '+'.join(id.split())
    payload = {
        'externalBorrowerId': id,
        'name': 'Exercise 2 test',
        'borrowerTypeId': '70BBD5E3-EDB7-4C28-A1C4-0F894EEA4467',
        'educationTypeId': educationTypeId,
        'countryId': countryId
    }
    resp = requests.post(url_format,  data=json.dumps(payload), headers=__my_headers__)
    if (resp.status_code == 201):
        result = resp.json()['id']
        click.echo("\nBorrower with id "+ id +" was created succesfully ✨")
        return result
    else:
       click.echo('Error 😬')
       click.echo(resp.json())

def createApplications(borrowerId, externalApplicationId, applicationDate):
    click.echo("\nCreating Application ⌛️ ...\n ")

    url_format = __host__ +'borrowers/'+borrowerId+'/applications'
    currencyId= chooseId('tables/currencies', 'currency')
    externalApplicationId = '+'.join(externalApplicationId.split())
    payload = {
        'externalApplicationId': externalApplicationId, 
        'applicationDate': applicationDate+ "T23:15:02.292Z",
        'requestedTerm': 3,
        'requestedTermUnitId': '246d03c8-ea99-406e-a32e-e5764e634a63',
        'productId': '462de2eb-0b30-4685-9686-0ac43295f72e',
        'currencyId': currencyId, 
    }
    resp = requests.post(url_format,  data=json.dumps(payload), headers=__my_headers__)
    if (resp.status_code == 201):
        result = resp.json()
        click.echo("\nApplication with id "+ externalApplicationId +" was created succesfully ✨")
        return result
    else:
       click.echo('Error 😬')
       click.echo(resp.json())

def createLoan(applicationId, externalLoanId, disbursementDate, currencyId):
    click.echo("\nCreating Loan ⌛️ ...\n ")

    url_format = __host__ +'loans'
    externalLoanId = '+'.join(externalLoanId.split())
    payload = {
        'externalLoanId': externalLoanId,
        'applicationId': applicationId,
        'loanTypeId': '3A0B59D1-864A-43A6-B860-56968EBB13E6',
        'disbursementDate': disbursementDate+ "T23:15:02.292Z",
        'interestRate': 0.2,
        'term': 3,
        'totalDisbursementAmount': 300,
        'fundId': '77a9139d-caab-43fd-aafb-3effc7652877',
        'termUnitId': '6575C4FF-32DC-4B62-BB9E-AC2C34DD55D3',
        'currencyId': currencyId,
        'loanStructureTypeId': 'E060ECE8-0446-45F3-B0ED-43A1F597755D',
        "paymentSchedule": [
            {
            "number": 1,
            "date": afterMonths(disbursementDate, 1)+"T23:04:33.691Z",
            "expectedPrincipal": 100,
            "expectedInterest": 20,
            "expectedVAT": 10
            },
            {
            "number": 2,
            "date": afterMonths(disbursementDate, 2)+"T23:04:33.691Z",
            "expectedPrincipal": 100,
            "expectedInterest": 20,
            "expectedVAT": 10
            },
            {
            "number": 3,
            "date": afterMonths(disbursementDate, 3)+"T23:04:33.691Z",
            "expectedPrincipal": 100,
            "expectedInterest": 20,
            "expectedVAT": 10
            },
        ]
    }
    resp = requests.post(url_format,  data=json.dumps(payload), headers=__my_headers__)
    if (resp.status_code == 201):
        result = resp.json()['id']
        click.echo("\nLoan with id "+ externalLoanId +" was created succesfully ✨")
        return result
    else:
       click.echo('Error 😬')
       click.echo(resp.json())

def createPayment(loanId, paymentId, paymentDate):
    click.echo("\nCreating payment ⌛️ ...\n ")
    paymentDate = tomorrow(paymentDate)
    url_format = __host__ +'loans/'+loanId+'/payments'
    paymentId = '+'.join(paymentId.split())
    print(paymentId)
    payload = json.dumps({
        "paymentId": paymentId,
        "paymentDate": paymentDate+"T23:15:02.292Z",
        "concepts": [
            {
            "conceptId": "91DC91A3-3D97-489B-AE32-8861D9D67D2C",
            "amount": 100
            },
            {
            "conceptId": "1BC5E871-3AE7-465A-9525-1D60DED6B381",
            "amount": 10
            },
            {
            "conceptId": "650F41F7-8CBB-4868-8843-B7020962F556",
            "amount": 20
            },
        ]
    })
    resp = requests.post(url_format,  data=payload, headers=__my_headers__)
    if (resp.status_code == 201):
        click.echo("\nPayment with id "+ paymentId +" was created succesfully ✨")
    else:
       click.echo('Error 😬')
       click.echo(resp.json())

##--------

@click.group()
def main():
    """
    Simple CLI for querying and create 
    """
    click.echo('\nBIENVENIDO(A) TO ACCIAL CLI🤓 IF YOU NEED HELP USE --help')
    click.echo('------------------------------------------------------------\n')
    pass

@main.command()
@click.argument('firstid')
@click.argument('secondid', default = 0)

@click.option('--borrower','value', flag_value='borrower',
              default=True)
@click.option('--application','value', flag_value='application')
@click.option('--loan','value', flag_value='loan',
              default=True)
@click.option('--payment','value', flag_value='payment')
def search(value, firstid, secondid):
    if value == "borrower":
       searchId("borrowers", firstid , 'externalBorrowerId');
    elif value == "application":
       searchId("borrowers/"+firstid+"/applications", secondid , 'externalApplicationId');
    elif value == "loan":
       searchId("loans/", firstid, 'externalLoanId');
    elif value == "payment":
       searchId("loans/"+firstid+"/payments", firstid, 'loanId');
    else:
       print("Code not found")



@main.command()
# @click.argument('id')
@click.option('--borrowerid', prompt='External Borrower Id: ', help='Id to create a borroewer')
@click.option('--applicationid', prompt='External Application Id: ', help='Id to create an application')
@click.option('--applicationdate', prompt='Date to aplication (yyyy-mm-dd): ', help='Application date must be less or equal than today', type=click.UNPROCESSED, callback=validate_date)
@click.option('--loanid', prompt='External Loand Id: ', help='Id to create a borroewer')
@click.option('--disbursementdate', prompt='Date to disbursement (yyyy-mm-dd): ', help='The disbursement date must be greater or equal than application date and less or equal than today', callback=validate_date_disbursement)
@click.option('--paymentid', prompt='External Payment Id: ', help='Id to create an payment')

def create(borrowerid, applicationid, applicationdate, loanid, disbursementdate, paymentid):
    borrowerIdCreated = createBorrower(borrowerid)
    applicationCreated = createApplications(borrowerIdCreated, applicationid,  applicationdate)
    if ('id' in applicationCreated):
        loanIdCreated = createLoan(applicationCreated['id'], loanid, disbursementdate, applicationCreated['currencyId'])
        createPayment(loanIdCreated , paymentid, disbursementdate)


if __name__ == '__main__':
    main()