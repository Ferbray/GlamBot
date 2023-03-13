import json
from aiohttp import ClientSession

api_access_token = 'TOKEN' #https://qiwi.com/api
my_login = 'Number phone' # номер QIWI Кошелька

async def qiwi_payment(pid, amount, blocked=["sum","account","comment"]):
	parameters = {"amount": str(amount), "currency": 643}
	parameters["extra['comment']"] = str(pid)
	parameters["extra['account']"] = my_login
	for block in blocked:
		parameters[f"blocked[{blocked.index(block)}]"] = block

	headers={"Authorization": 'Bearer ' + api_access_token}

	async with ClientSession(headers=headers) as session:
		async with session.get("https://qiwi.com/payment/form/99?", params = parameters) as response:
			return response.url
	
async def qiwi_history(payment_id):
	parameters = {'rows': 50, 'operation': "IN"}

	headers = {"Authorization": 'Bearer ' + api_access_token}

	async with ClientSession(headers=headers) as session:
		async with session.get('https://edge.qiwi.com/payment-history/v1/persons/'+my_login+'/payments', 
							 params = parameters) as history_json:
			pay_history = json.loads(await history_json.text())

	for hist in pay_history["data"]:
		if hist["comment"]==str(payment_id):
			return True
	return False
