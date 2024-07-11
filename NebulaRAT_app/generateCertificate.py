import errno
import os


# Path to the scripts
nebulaCert_path = os.path.join("nebulaScripts", "nebula-cert")       # ./nebula-cert print -path somecert.crt    to see certificate
nebulaScrptPath = os.path.join("nebulaScripts", "nebula")            # ./nebula-cert sign -name "laptop" -ip "192.168.100.5/24" -groups "laptop,ssh" to generate certificate
certificatesPath = os.path.join("nebulaFiles", "laptop1.crt")        # Path to store certificates

# output directory path
outputDir = "nebulaFiles"

# Parameters for testing
username = "admin2"
duration = "8h"
machineID = "laptop3"

#temporary function to get the required ip, TO BE REPLACED WITH ACTUAL FUNCTION THAT GETS THE IP FROM THE DATABASE
def get_required_ip(machineID):
    if machineID == "laptop1":
        return"192.168.100.101/24" 
    elif machineID == "laptop2":
        return "192.168.100.102/24"
    elif machineID == "laptop3":
        return "192.168.100.103/24"
    else:
        raise ValueError("Invalid machine ID.")

# print certificate function, prints the certificate to the console, returns nothing
# "certificate_path" is the path to the certificate
def print_certificate(certificate_path):
    # Check if the script and certificate exist
    if os.path.exists(nebulaCert_path) and os.path.exists(certificate_path):
        # Run the script with parameters
        os.system(f"{nebulaCert_path} print -path {certificate_path}")
    else:
        if not os.path.exists(nebulaCert_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), nebulaCert_path)
        elif not os.path.exists(certificate_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), certificate_path)

# generate certificate function, returns the path to the certificate
# "username" is the name of the machine that the certificate is being generated for
# "requiredIP" is the IP address of the machine that the certificate is being generated for
# "duration" is the duration is the time for which the certificate is valid
def generateCertificate(username, requiredIP, duration):
    from settings import path
    nebulaCert_path = os.path.realpath(os.path.join("nebulaScripts", "nebula-cert"))
    outputDir = os.path.realpath("nebulaFiles")
    # Check if the script exists
    print(os.getcwd())
    if os.path.exists(nebulaCert_path):
        # Run the script with parameters
        try:
            print(nebulaCert_path + " sign -name \"" + username + "\"" 
                                  + " -ip \"" + requiredIP + "\"" 
                                  + " -duration " + duration 
                                  + " -ca-crt " + os.path.join(outputDir, "ca.crt")
                                  + " -ca-key " + os.path.join(outputDir, "ca.key")
                                  + " -out-crt " + os.path.join(outputDir, username + ".crt")
                                  + " -out-key " + os.path.join(outputDir, username + ".key"))
            os.system(nebulaCert_path + " sign -name \"" + username + "\"" 
                                  + " -ip \"" + requiredIP + "\"" 
                                  + " -duration " + duration 
                                  + " -ca-crt " + os.path.join(outputDir, "ca.crt")
                                  + " -ca-key " + os.path.join(outputDir, "ca.key")
                                  + " -out-crt " + os.path.join(outputDir, username + ".crt")
                                  + " -out-key " + os.path.join(outputDir, username + ".key"))
        except Exception as e:
            raise Exception("Generate Certificate Error - " + str(e))
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), nebulaCert_path)
    
    return os.path.join(outputDir, username + ".crt"), os.path.join(outputDir, username + ".key"), outputDir


# the best option would be to return the certificate as a JSON object i need to see if there is a way to do it
# do we really need to print t
# he certificate on the web page? If not this function is not required
def get_certificate(certificate):
    # outdated
    '''os.chdir(outputDir)
    # Check if the script exists
    if os.path.exists(nebulaCert_path) and os.path.exists(certificate):
        # Run the script with parameters
        result = subprocess.run([nebulaCert_path, "print", "-path", certificate], capture_output=True, text=True)
        return result.stdout.strip()
    else:
        print("Print Certificate Error - Script or Certificate not found.")
        return None'''
    pass


# main defined for testing purposes only, TO BE REMOVED BEFORE DEPLOYMENT
def main():
    # remove the certificate and key if they already exist
    # nebula will refuse to overwrite existing files
    if os.path.exists(outputDir + username + ".crt"):
        os.remove(outputDir + username + ".crt")
        print("removed " + outputDir + username + ".crt")
    if os.path.exists(outputDir + username + ".key"):
        os.remove(outputDir + username + ".key")
        print("removed " + outputDir + username + ".key")

    # get the required IP for the machine, generate the certificate and print it
    requiredIP = get_required_ip(machineID)
    pathOfCert = generateCertificate(username, requiredIP, duration)
    print(pathOfCert)
    print_certificate(pathOfCert)

    # this is used to generate multiple certificates at once as per example given in the json file
    '''ip_addresses = ["192.168.100.101", "192.168.100.111", "192.168.100.112", "192.168.100.113", "192.168.100.121", "192.168.100.122"]
    for ip in ip_addresses:
        username = "admin_" + ip.split(".")[3]
        ip = ip + "/24"
        if os.path.exists(outputDir + username + ".crt"):
            os.remove(outputDir + username + ".crt")
            print("removed " + outputDir + username + ".crt")
        if os.path.exists(outputDir + username + ".key"):
            os.remove(outputDir + username + ".key")
            print("removed " + outputDir + username + ".key")

        filepath = generateCertificate(username, ip, "8h")
        print(filepath)
        print_certificate(filepath)'''

if __name__ == "__main__":
    main()