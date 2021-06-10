from logging import debug
from flask import Flask, request
from flask.json import jsonify
import nmap3
def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['GET'])
    def index():
        ip = ""
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            try:
                ip = request.environ['REMOTE_ADDR']
                with open('ip_list.txt',"w+") as fptr:
                    fptr.write(f"{ip}\n")

            except Exception as e:
                with open("error.log","w+") as fptr:
                    fptr.write(f"ERROR: {e}\n")
        else:
            try:
                ip = request.environ['HTTP_X_FORWARDED_FOR']
                with open("ip_list.txt","w+") as fptr:
                    fptr.write(f"{ip}\n")

            except Exception as e:
                with open("error.log","w+") as fptr:
                    fptr.write(f"ERROR: {e}\n")

        nmap = nmap3.NmapHostDiscovery()
        results = nmap.nmap_portscan_only(ip)
        try:
            with open("nmap_scans_logs.txt","w+") as fptr:
                fptr.write(f"ERROR: {results}\n")

        except Exception as e:
                with open("error.log","w+") as fptr:
                    fptr.write(f"ERROR: {e}\n")

        return "Hey This is a Flask Application"


    @app.route("/scans", methods=['GET'])
    def scans():
        lines = ""
        out = ""
        with open("nmap_scans_logs.txt","r") as fptr:
            lines = fptr.readlines()
        for line in lines:
            out = out + line.strip()
        return jsonify({"status" : 200, "scan_data" : out})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()