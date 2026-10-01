from flask import Flask, render_template, request
import qrcode
from io import BytesIO
from base64 import b64encode


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_qr():
    link = request.form.get("link", "").strip()

    if not link:
        return render_template(
            "index.html",
            error="Please enter a valid URL."
        )

    try:
        # Generate QR code
        qr_image = qrcode.make(link)

        # Store image in memory
        memory = BytesIO()
        qr_image.save(memory, format="PNG")
        memory.seek(0)

        # Convert image to Base64
        base64_image = (
            "data:image/png;base64,"
            + b64encode(memory.getvalue()).decode("ascii")
        )

        return render_template(
            "index.html",
            data=base64_image
        )

    except Exception as error:
        print(f"QR generation error: {error}")

        return render_template(
            "index.html",
            error="Unable to generate the QR code."
        )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
