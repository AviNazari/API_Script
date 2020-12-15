import json
import time

import requests

base_url = "https://testtask.3yourmind.com/api/v2.0/"
token = "792b74f003a2e05ae81eaae96b11a873b229ac40"
filename = "Left_arm.stl"  

std_header = {"Authorization": f"Token {token}"}


def create_basket():
    print("create_basket")
    r = requests.post(f"{base_url}user-panel/baskets/", headers=std_header)
    print(str(r.__dict__))
    return json.loads(r.content)["id"]


def create_line(basket_id):
    print("create_line")
    r = requests.post(
        f"{base_url}user-panel/baskets/{basket_id}/lines/", headers=std_header
    )
    print(str(r.__dict__))
    return json.loads(r.content)["id"]


def upload_file(basket_id, line_id):
    print("upload_file")
    params = {"basket_id": basket_id, "line_id": line_id}
    file = open(filename, "rb")
    r = requests.post(
        url=f"{base_url}files/",
        files={"file": (filename, file)},
        headers=std_header,
        params=params,
    )
    print(str(r.__dict__))
    wait_for_optimization(basket_id, line_id)
    return r


def wait_for_optimization(basket_id, line_id):
    print("wait_for_optimization")
    file_status = "pending"
    while file_status != "finished":
        time.sleep(1)
        r = requests.get(
            f"{base_url}user-panel/baskets/{basket_id}/"
            f"lines/{line_id}/file-status/",
            headers=std_header,
        )
        print(str(r.__dict__))
        file_status = json.loads(r.content)["status"]
    return


print("create_order")
basket_id = create_basket()
line_id = create_line(basket_id)
upload_file(basket_id, line_id)

