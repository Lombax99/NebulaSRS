tutte = "SELECT m.ip_addr, m.descrizione, r.cidr FROM MACCHINA m JOIN REGOLA as r ON r.macchina_id = m.id WHERE r.ca_name = 'Myorg, Inc';"
utenti = f"SELECT nome, cognome, username FROM UTENTE WHERE admin != :flag;"
mac  = "SELECT id, ip_addr, descrizione FROM MACCHINA;"

sel_macchine = f"""
        SELECT m.ip_addr, m.descrizione, r.cidr
        FROM UTENTE u
        JOIN USA as ua ON u.id = ua.utente_id
        JOIN MACCHINA as m ON ua.macchina_id = m.id
        JOIN REGOLA as r ON r.macchina_id = m.id
        WHERE u.username = :email
        AND r.ca_name='Myorg, Inc';
        """

firewall = f"""
        SELECT *
        FROM REGOLA AS R
        JOIN MACCHINA AS M ON M.ID = R.MACCHINA_ID
        WHERE M.IP_ADDR = :ip_addr;
        """

acc = f"""SELECT m.ip_addr
        FROM UTENTE u
        JOIN USA as ua ON u.id = ua.utente_id
        JOIN MACCHINA as m ON ua.macchina_id = m.id
        WHERE u.username = :email
        ORDER BY m.id;
        """

revocation = f"""SELECT ua.id, m.ip_addr, m.descrizione
        FROM UTENTE u
        JOIN USA as ua ON u.id = ua.utente_id
        JOIN MACCHINA as m ON ua.macchina_id = m.id
        WHERE u.username = :email
        ORDER BY m.id;
        """
