from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_region_and_id(account_id):
    url = 'https://recargajogo.com.br/api/auth/player_id_login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; moto g22 Build/STAS32.79-77-28-63-3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Mobile Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Android WebView";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?1',
        'Origin': 'https://recargajogo.com.br',
        'X-Requested-With': 'mark.via.gp',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://recargajogo.com.br/',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'source=mb; region=BR; mspid2=697c9e284e00ac32b36ba324b1f4f3cb; cc=true; datadome=r2V64Wrv_3eLPO80qhUWDIddDTPv5htTiIcL78574qqpKsnNQkJT5wuuPM2HjMVExS4~2o54Z0JF3BIWjuFiVXfiIcNQ6hV~NVCrp5dE_BgoJJLXtPmT14tayARU7jzj; session_key=lp9h69jq5xrg6sq3eatfuzb9roiukc3c'
    }
    payload = {"app_id": 100067, "login_id": account_id}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get('region'), data.get('nickname')
    else:
        return None, None

@app.route('/Region', methods=['GET'])
def region():
    account_id = request.args.get('uid')
    if not account_id:
        return jsonify({'error': Code 1'}), 400

    region, nickname = get_region_and_id(account_id)
    if region and nickname:
        return jsonify({'region': region, 'nickname': nickname}), 200
    else:
        return jsonify({'error': 'Code 2'}), 500

if __name__ == '__main__':
    app.run(debug=True)
