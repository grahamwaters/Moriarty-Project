from flask import Flask, render_template, request, redirect, url_for
import os
from gevent.pywsgi import WSGIServer
import re
import time
import threading
import asyncio
import subprocess
import Investigation

app = Flask(__name__)
options = {"phone_number": None, "find_owner": False, "social_media": False, "get_links": False, "spam_risk": False, "get_comments": False}

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        command = request.form["in"]
        process_command(command)
    return render_template("index.html")

def process_command(command):
    cmd, *args = command.split()
    if cmd == "help":
        return render_template("help.html")
    elif cmd == "add":
        return process_add_command(args)
    elif cmd == "show":
        return render_template("showoptions.html", **options)
    elif cmd == "run":
        return run_investigation()
    else:
        return render_template("unknown_command.html")

def process_add_command(args):
    if args[0] == "PhoneNumber":
        options["phone_number"] = "+" + re.search("\d+", args[1]).group(0)
        return render_template("phone_number_success.html", phone_number=options["phone_number"])
    elif args[0] == "feature":
        options[args[1]] = True
        return render_template(f"{args[1]}_success.html", phone_number=options["phone_number"])

def run_investigation():
    Investigation.general.location(options["phone_number"])
    threading.Thread(target=run_scripts).start()
    time.sleep(2)
    return redirect(url_for("investigation"))

def run_scripts():
    if options["spam_risk"]:
        Investigation.run_spam_risk(options["phone_number"])
    if options["get_comments"]:
        Investigation.run_get_comments(options["phone_number"])
    if options["get_links"]:
        Investigation.run_get_links(options["phone_number"])
    if options["find_owner"]:
        Investigation.run_find_owner(options["phone_number"])
    if options["social_media"]:
        Investigation.run_social_media(options["phone_number"])

@app.route("/investigation", methods=["GET"])
def investigation():
    data = Investigation.get_results(options["phone_number"])
    return render_template("result.html", **data)

if __name__ == "__main__":
    ip = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True).decode().strip()
    app.run(ip, 8080, debug=True)
