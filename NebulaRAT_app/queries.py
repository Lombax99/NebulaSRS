test = "SELECT ip_addr FROM CONF JOIN MACCHINA ON MACCHINA.CONF = CONF.ID WHERE MACCHINA.DESCRIZIONE = 'macchina1';"
tutte = "SELECT m.ip_addr, m.descrizione FROM MACCHINA m;"
utenti = "SELECT nome, cognome, username FROM UTENTE WHERE username != 'administration@admin.nebularat.com';"
mac  = "SELECT id, ip_addr, descrizione FROM MACCHINA;"

def build_query(type, x):

    if type == "firewall":
        transformed =f"""
        SELECT *
        FROM REGOLA AS R
        JOIN MACCHINA AS M ON M.ID = R.MACCHINA_ID
        WHERE M.IP_ADDR = '{x}';
        """
    elif type == "utente":
        transformed = f"""
        SELECT m.ip_addr, m.descrizione
        FROM UTENTE u
        JOIN USA as ua ON u.id = ua.utente_id
        JOIN MACCHINA as m ON ua.macchina_id = m.id
        WHERE u.username = '{x}';
        """
    elif type == "search_login":
        transformed = f"""
        SELECT username, password, nome, cognome
        FROM UTENTE
        WHERE username = '{x}';
        """
    elif type == "whois":
        transformed = f"""
        SELECT id, nome, cognome
        FROM UTENTE
        WHERE username = '{x}';
        """
    elif type == "acc":
        transformed = f"""SELECT m.ip_addr
        FROM UTENTE u
        JOIN USA as ua ON u.id = ua.utente_id
        JOIN MACCHINA as m ON ua.macchina_id = m.id
        WHERE u.username = '{x}'
        ORDER BY m.id;
        """
    elif type == "revocation":
        transformed = f"""SELECT ua.id, m.ip_addr, m.descrizione
        FROM UTENTE u
        JOIN USA as ua ON u.id = ua.utente_id
        JOIN MACCHINA as m ON ua.macchina_id = m.id
        WHERE u.username = '{x}'
        ORDER BY m.id;
        """
        
    return transformed
