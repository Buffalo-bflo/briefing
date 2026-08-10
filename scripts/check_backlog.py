import os
import sys

import requests

LIMITE = 20


def get_access_token():
    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": os.environ["GMAIL_CLIENT_ID"],
            "client_secret": os.environ["GMAIL_CLIENT_SECRET"],
            "refresh_token": os.environ["GMAIL_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def contar_sem_label(token):
    resp = requests.get(
        "https://gmail.googleapis.com/gmail/v1/users/me/threads",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": "in:inbox -has:userlabels", "maxResults": 100},
    )
    resp.raise_for_status()
    return resp.json().get("resultSizeEstimate", 0)


def main():
    token = get_access_token()
    count = contar_sem_label(token)
    print(f"Threads sem label na inbox: {count} (limite: {LIMITE})")
    if count > LIMITE:
        print("BACKLOG ACIMA DO LIMITE - a rotina diaria provavelmente falhou em algum dia anterior.")
        sys.exit(1)
    print("Backlog dentro do esperado.")


if __name__ == "__main__":
    main()
