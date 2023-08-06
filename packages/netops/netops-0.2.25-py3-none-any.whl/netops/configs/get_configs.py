import re
from click import command
import paramiko
import json

from lxml import etree
from jnpr.junos.exception import ConnectError
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_command
from nornir_paramiko.plugins.connections import Paramiko
from nornir_paramiko.plugins.tasks import paramiko_command

from ..utils.utils import (
    print_json,
    elem2dict
)
from .models import pyez_device

class TokenStack():
    def __init__(self):
        self._tokens = []

    def push(self, token):
        self._tokens.append(token)

    def pop(self):
        if not self._tokens:
            return None
        item = self._tokens[-1]
        self._tokens = self._tokens[:-1]
        return item

    def peek(self):
        if not self._tokens:
            return None
        return self._tokens[-1]

    def __str__(self):
        return " ".join(self._tokens)

    def __repr__(self):
        return " ".join(self._tokens)


def clean_config_str(config):
    """
    Clean config multiline string erasing RPC XML metadata
    
    Input:
            config: multiline config string
    Ouput:
            multiline config string without metadata
    """
    config_list = []
    for line in config.splitlines():
        if ('<' in line and '>' in line) or ('##' in line):
            continue
        else:
            config_list.append(line)
    return '\n'.join(config_list)


def convert_junos_text_to_set(config_str):
    """
    Parse out Juniper text format (JSON-like) into set format

    Input:
            config_str: multiline string of configuration statements in Junos text format
    Output:
            multiline string of configuration statements in Junos set format
    """
    config_str = clean_config_str(config_str)
    tokens = TokenStack()
    in_comment = False
    new_config = []

    for line_num, line in enumerate(config_str.splitlines()):
        if line.startswith("version ") or len(line) == 0:
            continue
        token = re.sub(r"^(.+?)#+[^\"]*$", r"\1", line.strip())
        token = token.strip()
        if (any(token.startswith(_) for _ in ["!", "#"])):
            # annotations currently not supported
            continue

        if token.startswith("/*"):
            # we're in a comment now until the next token (this will break if a multiline comment with # style { happens, but hopefully no-one is that dumb
            in_comment = True
            continue
        if "inactive: " in token:
            token = token.split("inactive: ")[1]
            new_config.append(f"deactivate {tokens} {token}")
        if token[-1] == "{":
            in_comment = False
            tokens.push(token.strip("{ "))
        elif token[-1] == "}":
            if not tokens.pop():
                print("Invalid json supplied: unmatched closing } encountered on line " + f"{line_num}")
                exit(1)
        elif token[-1] == ";":
            new_config.append(f"set {tokens} {token[:-1]}")
    if tokens.peek():
        print(tokens)
        print("Unbalanced JSON: expected closing }, but encountered EOF")
        exit(1)
    
    return "\n".join(new_config)


def junos_pyez_get_configs(nornir=None, dev_name=None, dev=None, get_print=False, format=None, filter_xml=None, model=True):
    """
    Get Junos device configs using Juniper PYEZ library.

    Input:
            nornir: nornir object
            dev_name: device name equal to the name available in nornir inventory
            dev: junos pyez device (used just if nornir and dev_name are not specified)
            get_print: boolean variable to print device configs
            format: junos pyez config output format (json, set, or default - xml)
            filter_xml: ???????
            model: boolean ?????????
    Output:
            d_data ou data_str: (str) config statements
    """
    d_data = None
    # When device is not directly given as an input
    if not dev:
        device = pyez_device(nornir, dev_name)   
    # When device is directly given as input
    else:
        device = dev

    # Connect to device
    try:
        device.open()
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        exit(1)
    except Exception as err:
        print(err)
        exit(1)

    # Set the default options to get configs
    options_default={'database' : 'committed'}
    options_custom = {}
    # XML format (default = None), Text format, Junos OS 'set' format or 'json' format
    if format:
        if format.lower() in ['text', 'set', 'json']:
            options_custom={ 'format': format.lower() }

    options={**options_default, **options_custom}

    # Parse model option as 'ietf', 'openconfig', 'custom' or True (default)
    if model == True:
        data = dev.rpc.get_config(model=True, options=options)
        valid_config = junos_pyez_check_configs(data, format)
        if not valid_config: # if config response is in wrong format exec again to convert
            # INVALID CONFIG - GET NEW CONFIG
            options['format']= 'text'
            data = dev.rpc.get_config(model=True, options=options)

    else:
        data = dev.rpc.get_config(filter_xml=filter_xml, model=model, options=options)
        valid_config = junos_pyez_check_configs(data, format)
        if not valid_config: # if config response is in wrong format exec again to convert
            # INVALID CONFIG - GET NEW CONFIG
            options['format']= 'text'
            data = dev.rpc.get_config(filter_xml=filter_xml, model=model, options=options)

    # Close device connection just if device was not directly provided
    device.close()

    # Convert config statements to string
    if format:
        if format.lower() in ['json']:
            data_str = data
        else:
            data_str = etree.tostring(data, encoding='unicode', pretty_print=True)
            if options['format'] != format:
                data_str = convert_junos_text_to_set(data_str)
    else: #default case
        # d_data is data in Python dictionary format
        d_data = elem2dict(data)
        data_str = etree.tostring(data, encoding='unicode', pretty_print=True)

    # Print config statements if get_print option is set
    if get_print:
        if d_data:
            print_json(d_data)
        else:
            print_json(data_str)

    # Return dictionary if default format option (format == None)
    if d_data:
        return d_data
    else:
        return data_str


def junos_pyez_check_configs(xml_data, format):
    """
    Check if Junos RPC response is correct based on format. If it is not, convert to correct format.
    
    Input:
            xml_data: lxml.etree node tree
            format: [None (default xml), 'text', 'set', 'json']
    Output:
            config_correct: boolean indicate if xml_data have been return in correct format
    """
    data_str = etree.tostring(xml_data, encoding='unicode', pretty_print=True)
    config_correct = True
    try:
        if format.lower() == 'set':
            config_correct = False
            for line in data_str.splitlines():
                if 'configuration' in line and 'set' in line:
                    config_correct = True
    except Exception: # If format is None (XML default)
        pass

    return config_correct


def junos_pyez_get_interfaces(config_dict):
    """
    Get configured interfaces from configuration dictionary <config_dict>, except of unavailable_interfaces.

    Input:
            config_dict: junos pyez configuration dictionary (json-like)
    Output:
            interfaces: list of configured interface names
    """
    unavailable_interfaces = ['gr', 'lo0', 'vlan', 'irb', 'ae']
    interfaces = []
    for interface in config_dict['configuration']['interfaces']['interface']:
        map_interface = True
        for una_int in unavailable_interfaces:
            if una_int in interface['name']:
                map_interface = False
                break
        if map_interface:
            interfaces.append(interface['name'])
    return interfaces


def junos_pyez_convert_configs_2_list(config_str, comp_strings):
    """
    Convert a multiline configuration string into a valid config statements list

    Input:
            config_str: multiline configuration string
            comp_strings: comparison strings that are not valid in config statement
    Output:
            config_list: list of valid configuration statements
    """
    config_lines = config_str.splitlines()
    configs_list = []
    for line in config_lines:
        valid_config = True
        for str_comp in comp_strings:
            if str_comp in line:
                valid_config = False
        if valid_config:
            configs_list.append(line)
    return configs_list


def linux_paramiko_get_configs(nornir=None, dev_name=None, format='json'):
    """
    Get Junos device configs using Juniper PYEZ library.

    Input:
            nornir: nornir object
            dev_name: device name equal to the name available in nornir inventory
            format: linux config output format (json, commands)
    Output:
            Logical Object (LO) config statements
    """
    # Get inventory data from Nornir
    nornir_host_data = nornir.inventory.hosts[dev_name].dict()
    host = nornir_host_data["hostname"]
    port = nornir_host_data["port"]
    username = nornir_host_data["username"]
    password = nornir_host_data["password"]
    
    #unavailable_interfaces = ['docker', 'lo', 'br', 'tunnel']
    # Set SSH Client connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    # Try to connect to host 3 times
    retry = True
    retry_num = 0
    max_retries = 3
    while retry:
        try:
            ssh.connect(host, port, username, password)
            retry = False
        except Exception as e:
            print(e)
            retry_num+=1
            if retry_num > max_retries:
                retry = False
    
    # Set linux configuration object
    configs = {
        'interface': {},
        'route': [],
    }
    # Set list of configuration statements for linux host
    config_commands = []
    
    # Get interface data from IP utility in linux
    show_int_command = "ip addr show"
    stdin, stdout, stderr = ssh.exec_command(show_int_command)
    lines = stdout.readlines()
    
    for line in lines:
        if 'UP' in line or 'DOWN' in line:
            interface = line.split(":")[1].replace(" ", "")
            configs['interface'][interface] = {'name': interface}
            configs['interface'][interface]['ipv4_addr'] = None
            configs['interface'][interface]['ipv6_addr'] = None
            if 'LOOPBACK' in line:
                admin_state = line.split('>')[0].split(',')[1]
            elif 'NO-CARRIER' not in line:
                admin_state = line.split('>')[0].split(',')[2]
            else:
                admin_state = line.split('>')[0].split(',')[3]
            configs['interface'][interface]['admin_state'] = admin_state
            configs['interface'][interface]['oper_state'] = line.split('state ')[1].split(' ')[0]

        if 'inet' in line and 'inet6' not in line:
            addr_list = line.split(" ")
            for str in addr_list:
                if "/" in str:
                    ipv4_addr = str
            configs['interface'][interface]['ipv4_addr'] = ipv4_addr
    
    for int in configs['interface']:
        if configs['interface'][int]['ipv4_addr']:
            config_commands.append(f"ifup {int}")
            config_commands.append(f"ip addr add {configs['interface'][int]['ipv4_addr']} dev {int}")

    # Get IP route commands
    show_route_command = "ip route show"
    stdin, stdout, stderr = ssh.exec_command(show_route_command)
    lines = stdout.readlines()

    for line in lines:
        config_route = line.split(' \n')[0]
        configs['route'].append(config_route)
        config_commands.append(f"ip route add {config_route}")
        #TODO add other routes

    # Close SSH connection
    ssh.close()

    if format == 'json':
        return configs
    elif format == 'commands':
        return '\n'.join(config_commands)
        


def linux_paramiko_get_interfaces(nornir_host=None):
    """
    Get Junos device configs using Juniper PYEZ library.

    Input:
            nornir: nornir object
            dev_name: device name equal to the name available in nornir inventory
    Output:
            Logical Object (LO) config statements
    """
    
    host = "200.159.254.86"
    port = 22
    username = "staff-pop"
    password = "rnppoprjabc123!!"

    show_command = "ip addr show"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(show_command)
    lines = stdout.readlines()
    interfaces_list = []
    for line in lines:
        if 'UP' in line or 'DOWN' in line:
            interfaces_list.append(line.split(":")[1].replace(" ", ""))
            
    return interfaces_list



    ############################
    # FINALIZAR GET INTERFACES E GET CONFIGS LINUX E CONSTRUIR DB
