import os
import subprocess

nebulaCert_path = "../nebulaScripts/nebula-cert"       # ./nebula-cert print -path somecert.crt    to see certificate
nebulaScrptPath = "../nebulaScripts/nebula"            # ./nebula-cert sign -name "laptop" -ip "192.168.100.5/24" -groups "laptop,ssh" to generate certificate
certificatesPath = "../nebulaFiles/laptop1.crt"        # Path to store certificates

# Parameters for testing
machineName = "admin2"
duration = "8h"
outputDir = "NebulaRAT_app/nebulaFiles/"
machineID = "laptop1"

#temporary function to get the required ip, TO BE REPLACED WITH ACTUAL FUNCTION
def get_required_ip(machineID):
    if machineID == "laptop1":
        return"192.168.100.100/24" 
    elif machineID == "laptop2":
        return "255.0.0.2/24"
    elif machineID == "laptop3":
        return "255.0.0.3/24"
    else:
        raise ValueError("Invalid machine ID.")


def print_certificate(certificate):
    # Check if the script exists
    if os.path.exists(nebulaCert_path) and os.path.exists(certificate):
        # Run the script with parameters
        os.system(nebulaCert_path + " print -path " + certificate)
    else:
        print("Print Certificate Error - Script or Certificate not found.")

#the best option would be to return the certificate as a JSON object i need to see if there is a way to do it
def get_certificate(certificate):
    os.chdir(outputDir)
    # Check if the script exists
    if os.path.exists(nebulaCert_path) and os.path.exists(certificate):
        # Run the script with parameters
        result = subprocess.run([nebulaCert_path, "print", "-path", certificate], capture_output=True, text=True)
        return result.stdout.strip()
    else:
        print("Print Certificate Error - Script or Certificate not found.")
        return None

def generateCertificate(machineName, requiredIP, duration):
    # Check if the script exists
    if os.path.exists(nebulaCert_path):
        # Run the script with parameters
        try:
            currentDir = os.getcwd()
            print("Current Directory:", currentDir)
            print(nebulaCert_path + " sign -name \"" + machineName + "\" -ip \"" + requiredIP + "\" -duration " + duration)
            os.system(nebulaCert_path + " sign -name \"" + machineName + "\" -ip \"" + requiredIP + "\" -duration " + duration)
        except Exception as e:
            print("Generate Certificate Error - " + str(e))
    else:
        print("Script not found.")





def main():
    os.chdir(outputDir)
    if os.path.exists(machineName + ".crt"):
        os.remove(machineName + ".crt")
    if os.path.exists(machineName + ".key"):
        os.remove(machineName + ".key")
    requiredIP = get_required_ip(machineID)
    generateCertificate(machineName, requiredIP, duration)
    print_certificate(machineName + ".crt")
    #print(get_certificate(machineName + ".crt"))

if __name__ == "__main__":
    main()