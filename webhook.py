from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

# 탭빗 웹훅용 시크릿 (환경 변수에 WEBHOOK_SECRET 으로 등록)
WEBHOOK_SECRET = os.getenv("TABBIT_WEBHOOK_SECRET", "")

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Tapbit-Signature", "")
    body      = request.get_data()

    # 서명 검증
    mac = hmac.new(WEBHOOK_SECRET.encode("utf-8"), body, hashlib.sha256)
    expected = mac.hexdigest()
    if not hmac.compare_digest(expected, signature):
        return "Invalid signature", 400

    event = request.json
    # TODO: 받은 이벤트(event)에 따라 처리 로직 추가
    print("Received webhook:", event)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
