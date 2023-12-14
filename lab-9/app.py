from flask import Flask, render_template, request
from src.smtp import send_email


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form = request.form
        recipient = form["recipient"]
        subject = form["subject"]
        body = form["body"]
        send_email(
            recipient=recipient,
            subject=subject,
            body=body
        )

        return render_template("index.html"), 200

    else:
        return render_template("index.html"), 200


def main():
    app.run()


if __name__ == "__main__":
    main()
