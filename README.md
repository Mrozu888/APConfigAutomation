# APConfigAutomation


## Setting up
Edit configuration in `config.json` file.
```json
{
  "VSZ_ADDRESS": "", 
  "ap_password": "", 
  "file_path": "template.xlsx", 
  "ap_subnet_target": "192.168.0.1", 
  "ap_netmask_target": "255.255.255.0", 
  "ap_subnet_to_find": "192.168.0.1/24" 
}
```
### Variables:

- **`VSZ_ADDRESS`**  
  Set the **vSZ (Virtual Smart Zone) address**. This is the address of the Virtual Smart Zone used to manage access points.

- **`ap_password`**  
  Set the **new password for the Access Point (AP)**. This password will be used to configure the AP remotely.

- **`file_path`**  
  Specify the path to the **Excel file** containing the AP configuration template. Modify the value if the file name or path is different.  
  Example: `"template.xlsx"`  

- **`ap_subnet_target`**  
  Set the **subnet address for the AP's Management Network**. This subnet will be used for configuring the AP's network settings.  
  Default: `"192.168.0.1"`

- **`ap_netmask_target`**  
  Set the **netmask for the AP's Management Network**. This is used to configure the subnet mask for the AP's management interface.  
  Default: `"255.255.255.0"`

- **`ap_subnet_to_find`**  
  Specify the **AP subnet** where the APs will be located. This is used to find the IP address of the APs within the given network range.  
  Default: `"192.168.0.1/24"`

### Install dependiences with:

```bash
pip install -r requirements.txt
```

## For Windows

[Npcap](https://npcap.com/#download) needed.

Run:
```bash
python main_windows.py
```


## For MacOS/Linux
```bash
sudo python main.py
```

