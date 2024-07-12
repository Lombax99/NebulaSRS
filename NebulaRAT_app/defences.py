import os

# Function to check for path traversal
# user_input: the file name to check
# dir_name: name of the directory to check for the file in
# can throw ValueError if no file is specified
def is_pathTraversal(user_input, dir_name="nebulaFiles"):
    current_dir = os.getcwd()
    # Define base path as a safe location for stored images   
    base_path = os.path.join(current_dir, dir_name)

    # Validate the parameter by checking if set
    if not user_input:
        raise ValueError("error: no file specified")
        
    # Construct the full path to the requested image file
    image_path = os.path.join(base_path, user_input)

    # Check that the file exists at the path, a path traversal could be detected here if the file does not exist
    if not os.path.isfile(image_path):
        return True

    # Get the real, absolute path to the file
    safe_path = os.path.realpath(image_path)

    common_base = os.path.commonpath([base_path, safe_path]) 
    if common_base != base_path:
        print("error: path traversal detected - common base")
        return True

    # Verify basename of resolved path matches original file
    if os.path.basename(safe_path) != user_input:
        # Invalid - path traversal detected
        print("error: path traversal detected - basename")
        return True

    # If all checks pass, return False
    return False


if __name__ == "__main__":
    if not os.getcwd().endswith("NebulaRAT_app"):
        os.chdir("NebulaRAT_app/")
    print("test 1: " + is_pathTraversal("../app.py"))        # should print "error: path traversal detected"
    print("test 2: " + is_pathTraversal("ca.crt"))           # should print the absolute path to ca.crt