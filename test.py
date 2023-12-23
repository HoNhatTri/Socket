import json

def read_config_json(filename):
    with open(filename, "r") as f:
        config = json.load(f)
    return config

# Sử dụng hàm để đọc file cấu hình
config = read_config_json('/home/vudeptrai/Documents/vu/config/config.json')

# In ra nội dung của username, password, host, port
username = (config["General"]["Username"])
password = (config["General"]["Password"])
host = (config["General"]["MailServer"])
port_smtp = (config["General"]["SMTP"])
port_pop3 = (config["General"]["POP3"])
print(username)
print(password)
print(host)
print(port_smtp)
print(port_pop3)