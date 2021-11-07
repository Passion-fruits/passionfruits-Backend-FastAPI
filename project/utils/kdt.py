from fastapi import HTTPException, status

from requests import get


def get_random_wallet():
    result = get("http://api.sonchaegeon.shop/kdt/wallet/random")

    if result.status_code == 200:
        response = result.json()
        return response["address"], response["private_key"]
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="could not get random wallet")
