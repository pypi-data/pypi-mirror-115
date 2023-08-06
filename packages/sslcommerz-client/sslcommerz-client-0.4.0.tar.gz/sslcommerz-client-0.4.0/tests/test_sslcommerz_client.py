import os
from pprint import pprint
from sslcommerz_client import SSLCommerzClient
from sslcommerz_client.dataclasses import APIConnectEnum, ResponseStatusEnum, Credential

STORE_ID = os.environ.get("STORE_ID")
STORE_PASSWD = os.environ.get("STORE_PASSWD")


IPN_DATA = {
    "amount": "41.00",
    "bank_tran_id": "21041820235217WSibg8WymA1Az",
    "base_fair": "0.00",
    "card_brand": "VISA",
    "card_issuer": "STANDARD CHARTERED BANK",
    "card_issuer_country": "Bangladesh",
    "card_issuer_country_code": "BD",
    "card_no": "421481XXXXXX4177",
    "card_sub_brand": "Classic",
    "card_type": "VISA-Dutch Bangla",
    "currency": "BDT",
    "currency_amount": "41.00",
    "currency_rate": "1.0000",
    "currency_type": "BDT",
    "error": "",
    "risk_level": "0",
    "risk_title": "Safe",
    "status": "VALID",
    "store_amount": "39.98",
    "store_id": "demo60755b72efb76",
    "tran_date": "2021-04-18 20:23:37",
    "tran_id": "29483c11198245a89f537aba38b0b2",
    "val_id": "2104182023530eW1BEsNECM6DtH",
    "value_a": "",
    "value_b": "",
    "value_c": "",
    "value_d": "",
    "verify_sign": "3cf600d3ea852dc9a292f8ef5b742aac",
    "verify_sign_sha2": "1bda6d3ff5a73f0998f12b4f0d0b120a42b99f380914f0e52274ffd5b9e40852",
    "verify_key": "amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_sub_brand,card_type,currency,currency_amount,currency_rate,currency_type,error,risk_level,risk_title,status,store_amount,store_id,tran_date,tran_id,val_id,value_a,value_b,value_c,value_d",
}

SESSION_INIT_DATA = {
    "total_amount": 100,
    "currency": "BDT",
    "tran_id": "221122",
    "product_category": "fashion",
    "success_url": "https://co.design",
    "fail_url": "https://co.design",
    "cancel_url": "https://co.design",
    "cus_name": "Utsob Roy",
    "cus_email": "roy@co.design",
    "shipping_method": "NO",
    "num_of_item": 1,
    "product_name": "Fancy Pants",
    "product_category": "Cloth",
    "product_profile": "physical-goods",
    "cus_add1": "bla",
    "cus_city": "Khulna",
    "cus_country": "Bangladesh",
    "cus_phone": "01558221870",
}


def test_session_initiation():
    client = SSLCommerzClient(
        store_id=STORE_ID, store_passwd=STORE_PASSWD, sandbox=True
    )
    resp = client.initiateSession(SESSION_INIT_DATA)
    assert resp.status_code == 200
    response = resp.response
    assert response.status == ResponseStatusEnum.SUCCESS


def test_get_transaction_by_sessionkey():
    client = SSLCommerzClient(
        store_id=STORE_ID, store_passwd=STORE_PASSWD, sandbox=True
    )

    initresp = client.initiateSession(SESSION_INIT_DATA)
    sessionkey = initresp.response.sessionkey
    resp = client.getTransactionBySession(sessionkey=sessionkey)

    assert resp.status_code == 200
    response = resp.response
    assert response.APIConnect == APIConnectEnum.DONE
    assert response.sessionkey == sessionkey


def test_get_transactions_by_transaction_id():
    client = SSLCommerzClient(
        store_id=STORE_ID, store_passwd=STORE_PASSWD, sandbox=True
    )
    resp = client.getTransactionsByID(IPN_DATA["tran_id"])

    assert resp.status_code == 200
    print(resp.raw_data.text)
    response = resp.response
    assert response.APIConnect == APIConnectEnum.DONE


def test_ipn_validation():
    client = SSLCommerzClient(
        store_id=STORE_ID, store_passwd=STORE_PASSWD, sandbox=True
    )
    status = client.validateIPN(IPN_DATA)
    hash = status.response.get_hash(Credential(**client.credential))
    assert hash == status.response.verify_sign
    assert status.status == True


def test_order_validation_data():
    data = {"val_id": IPN_DATA["val_id"]}
    client = SSLCommerzClient(
        store_id=STORE_ID, store_passwd=STORE_PASSWD, sandbox=True
    )
    resp = client.getOrderValidationData(data)
    assert resp.status_code == 200
    assert resp.response.val_id == data["val_id"]
