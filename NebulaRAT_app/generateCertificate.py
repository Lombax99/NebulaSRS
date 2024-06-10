import os

nebulaCert_path = "../nebulaScripts/nebula-cert"       # ./nebula-cert print -path somecert.crt    to see certificate
nebulaScrptPath = "../nebulaScripts/nebula"            # ./nebula-cert sign -name "laptop" -ip "192.168.100.5/24" -groups "laptop,ssh"
certificatesPath = "../nebulaFiles/laptop1.crt"        # Path to store certificates

machineName = "admin1"
duration = "8h"
outputDir = "NebulaRAT_app/nebulaFiles/"


def get_certificate_ip(name):
    if name == "laptop1":
        return"192.168.100.100/24" 
    elif name == "laptop2":
        return "255.0.0.2/24"
    elif name == "laptop3":
        return "255.0.0.3/24"
    else:
        raise ValueError("Invalid certificate name.")


def print_certificate(certificate):
    # Check if the script exists
    if os.path.exists(nebulaCert_path) and os.path.exists(certificate):
        # Run the script with parameters
        os.system(nebulaCert_path + " print -path " + certificate)
    else:
        print("Script not found.")


def generateCertificate():
    # Check if the script exists
    if os.path.exists(nebulaCert_path):
        # Run the script with parameters
        try:
            os.system(nebulaCert_path + " sign -name \"" + machineName + "\" -ip \"" + get_certificate_ip("laptop1") + "\" -duration " + duration)
        except Exception as e:
            print("invalid certificate name")
    else:
        print("Script not found.")


if os.path.exists("admin1.crt"):
    os.remove("admin1.crt")
if os.path.exists("admin1.key"):
    os.remove("admin1.key")
os.chdir(outputDir)
generateCertificate()
print_certificate(machineName + ".crt")
