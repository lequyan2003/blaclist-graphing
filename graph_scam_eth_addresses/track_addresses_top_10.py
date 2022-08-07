from requests import get

API_KEY = "D3EQ2J2FFTV4PVDGHRT4AK3AP1D4K1NA7P"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18

def make_api_url(module, action, address, **kwargs):
	url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

	for key, value in kwargs.items():
		url += f"&{key}={value}"

	return url

def get_transactions(address):
	transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
	response = get(transactions_url)
	data = response.json()["result"]

	internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
	response2 = get(internal_tx_url)
	data2 = response2.json()["result"]

	data.extend(data2)
	data.sort(key=lambda x: int(x['value']), reverse=True)

	edges = []
	duplicated = []

	for tx in data:
		if tx['from'] == address:
			if tx['to'] not in duplicated:
				edges.append((address, tx['to']))
				duplicated.append(tx['to'])
		else:
			if tx['from'] not in duplicated:
				edges.append((address, tx['from']))
				duplicated.append(tx['from'])
		
		if len(edges) == 10:
			break

	return edges

