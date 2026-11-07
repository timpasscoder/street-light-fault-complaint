from flask import Flask, render_template, request, redirect, url_for
import random
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")

    phone = request.form.get("phone")

    location = request.form.get("location")

    pincode = request.form.get("pincode")

    complaint = request.form.get("complaint")

    complaint_id = "SLF" + str(
        random.randint(1000, 9999)
    )

    status = "Pending"

    photo = request.files.get("photo")

    photo_filename = ""

    if photo and photo.filename:

        photo_filename = (
            complaint_id
            + "_"
            + photo.filename
        )

        photo.save(
            os.path.join(
                app.config[
                    "UPLOAD_FOLDER"
                ],
                photo_filename
            )
        )

    with open(
        "complaints.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{complaint_id}|"
            f"{name}|"
            f"{phone}|"
            f"{location}|"
            f"{pincode}|"
            f"{complaint}|"
            f"{status}|"
            f"{photo_filename}\n"
        )

    return render_template(
        "success.html",
        complaint_id=complaint_id
    )


@app.route(
    "/admin",
    methods=["GET", "POST"]
)
def admin():

    if request.method == "GET":

        return render_template(
            "admin_login.html"
        )

    password = request.form.get(
        "password"
    )

    if password != "admin123":

        return render_template(
            "admin_login.html",
            error="Wrong Password"
        )

    complaints = []

    try:

        with open(
            "complaints.txt",
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                data = (
                    line
                    .strip()
                    .split("|")
                )

                if len(data) >= 8:

                    complaints.append(
                        data
                    )

    except:

        pass

    return render_template(
        "admin.html",
        complaints=complaints
    )


@app.route("/update/<complaint_id>")
def update_status(
    complaint_id
):

    lines = []

    with open(
        "complaints.txt",
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    with open(
        "complaints.txt",
        "w",
        encoding="utf-8"
    ) as file:

        for line in lines:

            data = (
                line
                .strip()
                .split("|")
            )

            if (
                len(data) >= 8
                and
                data[0]
                ==
                complaint_id
            ):

                data[6] = "Fixed"

            file.write(
                "|".join(data)
                + "\n"
            )

    return redirect(
        url_for("admin")
    )


@app.route(
    "/track",
    methods=[
        "GET",
        "POST"
    ]
)
def track():

    complaint = None

    if request.method == "POST":

        cid = request.form.get(
            "cid"
        )

        try:

            with open(
                "complaints.txt",
                "r",
                encoding="utf-8"
            ) as file:

                for line in file:

                    data = (
                        line
                        .strip()
                        .split("|")
                    )

                    if (
                        len(data)
                        >= 8
                        and
                        data[0]
                        == cid
                    ):

                        complaint = data

                        break

        except:

            pass

    return render_template(
        "track.html",
        complaint=complaint
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )