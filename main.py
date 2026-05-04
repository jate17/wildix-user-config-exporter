import requests 
from bs4 import BeautifulSoup


ip = "" # Your IP DOG
start_index = 0
url = f"http://{ip}/index.php?class=classes/aclpbx/aclpbx.class.php"

params = {"skip-basic-auth-header": "true"}
headers = {
    "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "X-Requested-With": "XMLHttpRequest",
    "X-Prototype-Version": "1.6.1",
    "DNT": "1",
    "Referer": "http://{ip}/?Menuid=10",
}
cookies = {"PHPSESSID": ""}# Your PHPSESSID DOG 
serial_number = "" #Your s/n DOG
uid = []

while True:
    response = requests.get(f"{url}&newclass=aclpbx&action=getUsers&startIndex={start_index}&results=20&sortKey=&sortDir=asc&search=&pbxSerial={serial_number}", params=params, headers=headers, cookies=cookies)
    data = response.json()
    [uid.append(x["uid"]) for x in data["BODY"] ]
    if len(data["BODY"]) == 20: 
        print(99999)
        start_index += 20
    else: 
        break

type_in = {
    0 : "input", #Status
    1 : "select", # Get selected
    2 : "textarea",
    3 : "select",#Get all
    4 : "input", #Text
    5 : "div > img" # Doesn't work
}

def grapValue(id, s_id = None, typetograp = 0):
    idtofind = soup.find(type_in[typetograp], id = id)
    if typetograp == 0:
        if idtofind.attrs["value"] == "1":
            if s_id != None: 
                return soup.find("input", id = s_id).attrs["value"]
            return True
        return False
    elif typetograp == 1: 
        return idtofind.find_all('option', selected=True)[0].get_text()
    elif typetograp == 2: 
        return soup.find(type_in[typetograp], id = id).get_text().split("\n")
    elif typetograp == 3: 
        return [ x.get_text() for x in idtofind.find_all('option', selected=False)]
    elif typetograp == 4: 
        return soup.find(type_in[typetograp], id = id).attrs['value']
    elif typetograp == 5:   
        return soup.find(type_in[typetograp], id = id)#.attrs['src']


employe = {}

for x in uid:
    url = f"http://{ip}/features/features_user.php?userid={x}&admin=1"

    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    html = response.text


    soup = BeautifulSoup(html, 'html.parser')


    output = {
        "reject": grapValue("REJECT"),
        "ucf":  grapValue("status_UCF", "UCF"),
        "bcf": grapValue("status_BCF", "BCF"),
        "fcf": grapValue("status_FCF", "FCF"),
        "cw": grapValue("CW"),
        "timeout": grapValue("status_TOUT", "TOUT"),
        "mext": grapValue("status_MEXT", "MEXT"),
        "mext_conf": grapValue("MOBCONFIRMATION"),
        "email_notify": grapValue("EMAILMCN"), 
        "sms_notify": grapValue("SMSMCN"),
        "ring": grapValue("status_RING", "RING"),
        "shared_vociemail": grapValue("status_SHAREDVM","SHAREDVM"),
        "hotline": grapValue("status_HOTLINE","HOTLINE"),
        "delay_hotline": grapValue("delay_HOTLINE"),
        "cwtone": grapValue("CWTONE"),
        "road": grapValue("ROAD"),
        "unread_messages_via_email": grapValue("unread_messages_via_email"),
        "twofactor": grapValue("TWOFACTOR", None, 1),
        "phonebook_lp": grapValue("__LPHONEBOOK", None, 3),
        "phonebook_rp": grapValue("__RPHONEBOOK", None, 3),
        "datetime_format": grapValue("DATETIME_format", None, 1),
        "datetime_is24h": grapValue("DATETIME_is24h", None, 1),
        "popup_url": grapValue("POPUPURL",None, 4),
        "open_popup_incoming_calls_when": grapValue("open_popup_incoming_calls_when", None, 1),
        "open_popup_outgoing_calls_when": grapValue("open_popup_outgoing_calls_when", None, 1),
        "fkeys": grapValue("FKEYS", None, 2),
        "defstatus": grapValue("DEFSTATUS", None, 2),
        "LcallGroupsWhitelist": grapValue("__LcallGroupsWhitelist", None, 3),
        "RcallGroupsWhitelist": grapValue("__RcallGroupsWhitelist", None, 3),
        "CALLCENTER_MODE": grapValue("CALLCENTER_MODE"),
        "statusSync": grapValue("statusSync"),
        "LcallGroups": grapValue("__LcallGroups", None, 3),
        "RcallGroups": grapValue("__RcallGroups", None, 3),
        "fax_options_from_company": grapValue("fax_options_from_company", None, 4),
        "fax_options_stationid": grapValue("fax_options_stationid", None, 4),
        "fax_options_headerinfo": grapValue("fax_options_headerinfo", None, 4),
        "fax_faxcover_uploader_image": grapValue("fax_faxcover_uploader_image", None, 5),
        "fax_faxcover_uploader_image": grapValue("fax_faxcover_uploader_image", None, 5),
        "callgroups": grapValue("callgroups", None, 2),
        "pickupgroups": grapValue("pickupgroups", None, 2),
        "custom_identities": grapValue("custom_identities", None, 4),
        "LROSTER": grapValue("__LROSTER", None, 3),
        "RROSTER": grapValue("__RROSTER", None, 3),

    }

    employe[x] = output



print(employe)

