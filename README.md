# APConfigAutomation


## Setting up
Edit configuration in `config.json` file.
```json
{
  "VSZ_ADDRESS": "", // set vSZ address
  "ap_password": "", // set AP new password
  "file_path": "template.xlsx", // modify if other file name
  "ap_subnet_target": "192.168.0.1", // set AP MGMT network
  "ap_netmask_target": "255.255.255.0", // set AP MGMT netmask
  "ap_subnet_to_find": "192.168.0.1/24" // specify AP subnet with AP to configure
}
```

Install dependiences with:
```bash
pip install -r requirements.txt
```

## For Windows

[Npcap](https://npcap.com/#download) needed.

Run:
```bash
python .\main_windows.py
```


## For MacOS/Linux
```bash
sudo python main.py
```

