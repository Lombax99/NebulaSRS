test = "SELECT * FROM TEST;"

def build_query(type, x):
    if type == "firewall":
        transformed =f"""
        SELECT *
        FROM REGOLA AS R
        JOIN CONF AS C ON C.ID = R.CONF_ID
        WHERE C.IP_ADDR = '{x}';
        """
    else:
        transformed = f"""
        SELECT c.ip_addr, m.descrizione
        FROM UTENTE u
        JOIN USA as ua ON u.id = ua.utente_id
        JOIN MACCHINA as m ON ua.macchina_id = m.id
        JOIN CONF as c ON m.conf = c.id
        WHERE u.username = '{x}';
        """
    return transformed