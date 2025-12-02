from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )

@app.route("/")
def home():
    return "API Flask Railway OK!"

@app.route("/getall", methods=["GET"])
def getall():
    try:
        conn = connect_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM dulieu")
        rows = cur.fetchall()
        conn.close()
        return jsonify({"success": True, "data": rows})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.get_json()
        ngay = data.get("ngay")
        stt = data.get("stt")
        tenhang = data.get("tenhang")
        soluong = data.get("soluong")
        page = data.get("page")
        pageName = data.get("pageName")

        conn = connect_db()
        cur = conn.cursor()
        sql = "INSERT INTO dulieu (ngay, stt, tenhang, soluong, page, pageName) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (ngay, stt, tenhang, soluong, page, pageName))
        # cur.execute("INSERT INTO your_table (name,amount) VALUES (%s,%s)", (name,amount))
        conn.commit()
        conn.close()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
@app.route("/upload_bulk", methods=["POST"])
def upload_bulk():
    try:
        items = request.get_json()

        if not items:
            return jsonify({"success": False, "error": "No data received"})

        conn = connect_db()
        cur = conn.cursor()

        sql = """
            INSERT INTO dulieu (ngay, stt, tenhang, soluong, page, pageName)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        for item in items:
            cur.execute(sql, (
                item.get("ngay"),
                item.get("stt"),
                item.get("tenhang"),
                item.get("soluong"),
                item.get("page"),
                item.get("pageName")
            ))

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": f"Đã nhận {len(items)} dòng và lưu vào Aiven."
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
