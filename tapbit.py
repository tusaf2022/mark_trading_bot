import os
import time
import hmac
import hashlib
import requests

# 환경 변수에서 읽기
API_KEY    = os.getenv("TABBIT_API_KEY")
API_SECRET = os.getenv("TABBIT_SECRET") or ""
BASE_URL   = "https://api.tapbit.io"

def get_account_info():
    """ 계정 정보 조회 """
    path   = "/v1/account/info"
    params = {
        "accessid": API_KEY,
        "tonce": str(int(time.time() * 1000))
    }
    # 서명 생성
    query = "&".join(f"{k}={v}" for k, v in params.items())
    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        query.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    params["signature"] = signature

    url = BASE_URL + path
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    info = get_account_info()
    print("Account Info:", info)
