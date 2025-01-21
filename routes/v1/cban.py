from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_region(account_id):
    url = f"https://api.prates.xyz/v1/region"
    params = {"uid": account_id}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("region")
        else:
            print("Erro ao obter a região:", response.status_code)
            return None
    except Exception as e:
        print("Erro na solicitação da região:", e)
        return None

def check_ban_status(region, account_id):
    url = "https://ff.garena.com/api/antihack/check_banned"
    params = {
        'lang': region,
        'uid': account_id
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 12; moto g22 Build/STAS32.79-77-28-63-4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.106 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-platform': "\"Android\"",
        'x-requested-with': "B6FksShzIgjfrYImLpTsadjS86sddhFH",
        'sec-ch-ua': "\"Chromium\";v=\"130\", \"Android WebView\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?1",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://ff.garena.com/pt/support",
        'accept-language': "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        'priority': "u=1, i"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            is_banned = data.get("data", {}).get("is_banned")
            period = data["data"].get("period") if is_banned == 1 else None
            return is_banned == 1, period
        else:
            print("Erro ao verificar o banimento:", response.status_code)
            return None, None
    except Exception as e:
        print("Erro na solicitação de banimento:", e)
        return None, None

@app.route('/check_ban', methods=['GET'])
def check_ban():
    account_id = request.args.get('uid')
    if not account_id:
        return jsonify({'error': 'Parâmetro UID é obrigatório'}), 400

    region = get_region(account_id)
    if not region:
        return jsonify({'error': 'Não foi possível obter a região'}), 500

    is_banned, ban_period = check_ban_status(region, account_id)
    if is_banned is None:
        return jsonify({'error': 'Não foi possível verificar o status de banimento'}), 500

    return jsonify({
        'is_banned': is_banned,
        'ban_period': ban_period if is_banned else None
    })

if __name__ == '__main__':
    app.run(debug=True)
