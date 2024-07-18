import errno
import os

# generate certificate function, returns the path to the certificate
# "username" is the name of the machine that the certificate is being generated for
# "requiredIP" is the IP address of the machine that the certificate is being generated for
# "duration" is the duration is the time for which the certificate is valid
def generate_Certificate(username, requiredIP, duration):
    requiredIP = requiredIP.split("/")[0] + "/24"
    print(requiredIP)
    nebulaCert_path = os.path.join("nebulaScripts", "nebula-cert")
    outputDir = "nebulaFiles"
    # Check if the script exists
    if os.path.exists(nebulaCert_path):
        # Run the script with parameters
        try:
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


if __name__ == "__main__":
    print(generate_Certificate("test", "192.168.100.121/32", "8h"))