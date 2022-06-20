import uuid
import requests
from decouple import config

from hash_utils import sign_message


def payout_handler(data):
    request_id = str(
        uuid.uuid4()
    )  # FIXME: recommend from night-pay PartnerID + 9P + YYYYMMDD + UniqueId
    message = "|".join(
        (
            request_id,
            config("HALONGPAY_PARTNER_ID"),
            data["bank_no"],
            data["account_no"],
            str(data["account_type"]),
            data["account_name"],
            str(data["amount"]),
            data["content"],
        )
    )
    signature = sign_message(message)
    res = requests.post(
        config("NIGHT_PAY_ENDPOINT"),
        json={
            **data,
            "request_id": request_id,
            "partner_id": config("HALONGPAY_PARTNER_ID"),
            "signature": signature,
        },
    )
    # TODO: dispatch result somewhere to show result to the user
    print(res.content)
