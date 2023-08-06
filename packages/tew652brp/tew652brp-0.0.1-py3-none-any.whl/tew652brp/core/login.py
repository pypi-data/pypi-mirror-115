def login(session, url, username, password):
    resp = session.post(url, data={'username': username, 'password': password})
    return 'status.htm' in resp.text

