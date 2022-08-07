from requests import get

API_KEY = "D3EQ2J2FFTV4PVDGHRT4AK3AP1D4K1NA7P"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18

def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup

def make_api_url(module, action, address, **kwargs):
	url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

	for key, value in kwargs.items():
		url += f"&{key}={value}"

	return url

def get_account_balance(address):
	balance_url = make_api_url("account", "balance", address, tag="latest")
	response = get(balance_url)
	data = response.json()

	value = int(data["result"]) / ETHER_VALUE
	return value

def get_transactions(address):
	transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
	response = get(transactions_url)
	data = response.json()["result"]

	internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
	response2 = get(internal_tx_url)
	data2 = response2.json()["result"]

	data.extend(data2)
	data.sort(key=lambda x: int(x['timeStamp']))

	tmp = {
		address: []
	}

	output = {
		address: []
	}

	duplicated_tx = []

	for tx in data:
		tuple_tx_addresses = (tx['from'], tx['to'])
		tmp[address].append(tuple_tx_addresses)

	tmp[address] = list(set(tmp[address]))

	for i in range(0, len(tmp[address])):
		for j in range(1, len(tmp[address])):
			if tmp[address][i] == Reverse(tmp[address][j]):
				duplicated_tx.append(tmp[address][j])
		if tmp[address][i] not in duplicated_tx:
			output[address].append(tmp[address][i])

	return output[address]
