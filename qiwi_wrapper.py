import json
import requests

api_access_token = '9e6ddfa3f901d1a7a52ecbd42bcfd9c1' #https://qiwi.com/api
my_login = '+79619352257' # номер QIWI Кошелька

async def qiwi_payment(pid,amount,blocked=["sum","account","comment"]):
	session = requests.Session()
	session.headers['authorization'] = 'Bearer ' + api_access_token
	url=f"https://qiwi.com/payment/form/99?"
	parameters={"amount": amount,"currency": 643}
	parameters["extra['comment']"]=pid
	parameters["extra['account']"]=my_login
	for block in blocked:
		parameters[f"blocked[{blocked.index(block)}]"]=block
#	parameters["extra['accountType']"]='phone'
	pay_url = session.get(url, params = parameters)
	return pay_url.url
	
async def qiwi_history():
	session = requests.Session()
	session.headers['authorization'] = 'Bearer ' + api_access_token
	parameters = {'rows': 50, 'operation': "IN"}
	history_json = session.get('https://edge.qiwi.com/payment-history/v1/persons/'+my_login+'/payments', params = parameters)
	pay_history=json.loads(history_json.text)
	return pay_history

#async def payment_history_transaction(transaction_id):
#    session = requests.Session()
#    session.headers['authorization'] = 'Bearer ' + api_access_token  
#    parameters = {'type': "IN"}
#    history_json = session.get('https://edge.qiwi.com/payment-history/v1/transactions/'+str(transaction_id), params = parameters)
#    pers_history=json.loads(history_json.text)
#    return pers_history
