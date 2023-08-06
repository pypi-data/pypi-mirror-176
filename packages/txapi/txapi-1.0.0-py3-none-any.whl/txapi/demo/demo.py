# -*- coding:utf-8 -*-
from api import API
import config

client = API.v3(
    api_domain=config.api_domain,
    region=config.region,
    secret_id=config.sid,
    secret_key=config.skey,
    debug=config.is_debug,
    ssl=config.is_ssl)

cvm = client.get_client("cvm", "2017-03-12")

params = {
    "Limit": 20,
    "Offset": 1
}
print(cvm.request("DescribeInstances", params))