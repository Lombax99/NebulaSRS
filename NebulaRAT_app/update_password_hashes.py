import json
import bcrypt

# Funzione per verificare se una password è già hashata
def is_hashed(password):
    return password.startswith('$2b$')

# Funzione per generare l'hash della password
def generate_password_hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Funzione per aggiornare il file JSON con l'hash delle password
def update_json_with_password_hashes(json_file):
    with open(json_file, 'r+') as file:
        data = json.load(file)
        updated_data = []

        for entry in data:
            if 'password' in entry and not is_hashed(entry['password']):
                hashed_password = generate_password_hash(entry['password'])
                entry['password_hash'] = hashed_password
                del entry['password']
            updated_data.append(entry)

        file.seek(0)
        json.dump(updated_data, file, indent=4)
        file.truncate()


if __name__ == "__main__":
    json_file = 'nebulaFiles/users.json'
    update_json_with_password_hashes(json_file)
    print(f"File JSON aggiornato con successo: {json_file}")
