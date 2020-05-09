import json
from aiohttp import ClientSession

api_access_token = '9e6ddfa3f901d1a7a52ecbd42bcfd9c1' #https://qiwi.com/api
my_login = '+79619352257' # номер QIWI Кошелька

async def qiwi_payment(pid, amount, blocked=["sum","account","comment"]):
	parameters={"amount": amount, "currency": 643}
	parameters["extra['comment']"] = pid
	parameters["extra['account']"] = my_login
	for block in blocked:
		parameters[f"blocked[{blocked.index(block)}]"] = block

	async with ClientSession() as session:
		session.headers['authorization'] = 'Bearer ' + api_access_token
		async with session.get("https://qiwi.com/payment/form/99?", params = parameters) as response:
			return response.url
	
async def qiwi_history(payment_id):
	parameters = {'rows': 50, 'operation': "IN"}
	async with ClientSession() as session:
		session.headers['authorization'] = 'Bearer ' + api_access_token
		async with session.get('https://edge.qiwi.com/payment-history/v1/persons/'+my_login+'/payments', 
							 params = parameters) as history_json:
			pay_history=json.loads(history_json.text)

	for hist in pay_history:
		if hist["comment"]==str(payment_id):
			return True
	return False