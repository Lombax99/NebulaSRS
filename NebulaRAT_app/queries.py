test = "SELECT ip_addr FROM CONF JOIN MACCHINA ON MACCHINA.CONF = CONF.ID WHERE MACCHINA.DESCRIZIONE = 'macchina1';"

def build_query(type, x):

    if type == "firewall":
        transformed =f"""
        SELECT *
        FROM REGOLA AS R
        JOIN MACCHINA AS M ON M.ID = R.MACCHINA_ID
        WHERE M.IP_ADDR = '{x}';
        """
    elif type == 'utente':
        transformed = f"""
        SELECT m.ip_addr, m.descrizione
        FROM UTENTE u
        JOIN USA as ua ON u.id = ua.utente_id
        JOIN MACCHINA as m ON ua.macchina_id = m.id
        WHERE u.username = '{x}';
        """
    elif type == 'search_login':
        transformed = f"""
        SELECT username, password, nome, cognome
        FROM UTENTE
        WHERE username = '{x}';
        """
    return transformed