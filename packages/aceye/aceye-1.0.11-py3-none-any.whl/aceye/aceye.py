import os
import json
import requests
import rich_click as click
import yaml
import urllib3
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

urllib3.disable_warnings()

class ACEye():
    def __init__(self,
                url,
                username,
                password):
        self.aci = url
        self.username = username
        self.password = password

    def aceye(self):
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'Tenant/JSON')
        if not os.path.exists(final_directory):
            os.mkdirs(final_directory)
            # os.mkdir("/Tenant/YAML")
            # os.mkdir("/Tenant/CSV")
            # os.mkdir("/Tenant/HTML")
            # os.mkdir("/Tenant/Markdown")
            # os.mkdir("/Tenant/Mindmap")
            # os.mkdir("/Application Profiles/JSON")
            # os.mkdir("/Application Profiles/YAML")
            # os.mkdir("/Application Profiles/CSV")
            # os.mkdir("/Application Profiles/HTML")
            # os.mkdir("/Application Profiles/Markdown")
            # os.mkdir("/Application Profiles/Mindmap")
            # os.mkdir("/Bridge Domains/JSON")
            # os.mkdir("/Bridge Domains/YAML")
            # os.mkdir("/Bridge Domains/CSV")
            # os.mkdir("/Bridge Domains/HTML")
            # os.mkdir("/Bridge Domains/Markdown")
            # os.mkdir("/Bridge Domains/Mindmap")
            # os.mkdir("/Contexts/JSON")
            # os.mkdir("/Contexts/YAML")
            # os.mkdir("/Contexts/CSV")
            # os.mkdir("/Contexts/HTML")
            # os.mkdir("/Contexts/Markdown")
            # os.mkdir("/Contexts/Mindmap")
            # os.mkdir("/Endpoints/JSON")
            # os.mkdir("/Endpoints/YAML")
            # os.mkdir("/Endpoints/CSV")
            # os.mkdir("/Endpoints/HTML")
            # os.mkdir("/Endpoints/Markdown")
            # os.mkdir("/Endpoints/Mindmap")
            # os.mkdir("/EPG/JSON")
            # os.mkdir("/EPG/YAML")
            # os.mkdir("/EPG/CSV")
            # os.mkdir("/EPG/HTML")
            # os.mkdir("/EPG/Markdown")
            # os.mkdir("/EPG/Mindmap")
            # os.mkdir("/L3Outs/JSON")
            # os.mkdir("/L3Outs/YAML")
            # os.mkdir("/L3Outs/CSV")
            # os.mkdir("/L3Outs/HTML")
            # os.mkdir("/L3Outs/Markdown")
            # os.mkdir("/L3Outs/Mindmap")
            # os.mkdir("/Subnets/JSON")
            # os.mkdir("/Subnets/YAML")
            # os.mkdir("/Subnets/CSV")
            # os.mkdir("/Subnets/HTML")
            # os.mkdir("/Subnets/Markdown")
            # os.mkdir("/Subnets/Mindmap")
            # os.mkdir("/Top System/JSON")
            # os.mkdir("/Top System/YAML")
            # os.mkdir("/Top System/CSV")
            # os.mkdir("/Top System/HTML")
            # os.mkdir("/Top System/Markdown")
            # os.mkdir("/Top System/Mindmap")  
        self.cookie = self.get_token()
        parsed_json = json.dumps(self.tenants(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.epgs(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bridge_domains(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.contexts(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.application_profiles(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.l3outs(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.topSystem(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.subnets(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.endpoints(), indent=4, sort_keys=True)
        self.all_files(parsed_json)

    def get_token(self):
        url = f"{ self.aci }/api/aaaLogin.json"
        payload = json.dumps({
            "aaaUser": {
                "attributes": {
                "name": f"{ self.username }",
                "pwd": f"{ self.password }"
                }
            }
        })

        response = requests.request("POST", url, data=payload, verify=False)
        print(f"<Authentication Status code {response.status_code} for { url }>")
        return response.cookies

    def tenants(self):
        self.url = f"{ self.aci }/api/node/class/fvTenant.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Tenant Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def epgs(self):
        self.url = f"{ self.aci }/api/node/class/fvAEPg.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<EPG Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def bridge_domains(self):
        self.url = f"{ self.aci }/api/node/class/fvBD.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Bridge Domains Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def contexts(self):
        self.url = f"{ self.aci }/api/node/class/fvCtx.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Contexts Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)        

    def application_profiles(self):
        self.url = f"{ self.aci }/api/node/class/fvAp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Application Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)    
    
    def l3outs(self):
        self.url = f"{ self.aci }/api/node/class/l3extOut.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<L3Outs Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)     

    def topSystem(self):
        self.url = f"{ self.aci }/api/node/class/topSystem.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Top System Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def subnets(self):
        self.url = f"{ self.aci }/api/node/class/fvSubnet.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Subnet Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def endpoints(self):
        self.url = f"{ self.aci }/api/node/class/fvCEp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Connected Endpoints Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def json_file(self, parsed_json):
        if "Tenant" in self.url:
            with open('Tenant/JSON/Tenants.json', 'w' ) as f:
                f.write(parsed_json)

        if "AEPg" in self.url:
            with open('EPG/JSON/EPGs.json', 'w' ) as f:
                f.write(parsed_json)

        if "BD" in self.url:
            with open('Bridge Domains/JSON/Bridge Domains.json', 'w' ) as f:
                f.write(parsed_json)

        if "Ctx" in self.url:
            with open('Contexts/JSON/Contexts.json', 'w' ) as f:
                f.write(parsed_json)

        if "Ap" in self.url:
            with open('Application Profiles/JSON/Application Profiles.json', 'w' ) as f:
                f.write(parsed_json)

        if "l3extOut" in self.url:
            with open('L3Outs/JSON/L3Outs.json', 'w' ) as f:
                f.write(parsed_json)

        if "topSystem" in self.url:
            with open('Top System/JSON/Top System.json', 'w' ) as f:
                f.write(parsed_json)

        if "Subnet" in self.url:
            with open('Subnets/JSON/Subnets.json', 'w' ) as f:
                f.write(parsed_json)

        if "CEp" in self.url:
            with open('Endpoints/JSON/Endpoints.json', 'w' ) as f:
                f.write(parsed_json)

    def yaml_file(self, parsed_json):
        clean_yaml = yaml.dump(json.loads(parsed_json), default_flow_style=False)
        if "Tenant" in self.url:
            with open('Tenant/YAML/Tenants.yaml', 'w' ) as f:
                f.write(clean_yaml)        

        if "AEPg" in self.url:
            with open('EPG/YAML/EPGs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "BD" in self.url:
            with open('Bridge Domains/YAML/Bridge Domains.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "Ctx" in self.url:
            with open('Contexts/YAML/Contexts.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "Ap" in self.url:
            with open('Application Profiles/YAML/Application Profiles.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "l3extOut" in self.url:
            with open('L3Outs/YAML/L3Outs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "topSystem" in self.url:
            with open('Top System/YAML/Top System.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "Subnet" in self.url:
            with open('Subnets/YAML/Subnets.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "CEp" in self.url:
            with open('Endpoints/YAML/Endpoints.yaml', 'w' ) as f:
                f.write(clean_yaml)

    def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        csv_template = env.get_template('aci_csv.j2')      
        csv_output = csv_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json))
        if "Tenant" in self.url:                                         
            with open('Tenant/CSV/Tenants.csv', 'w' ) as f:
                f.write(csv_output)

        if "AEPg" in self.url:
            with open('EPG/CSV/EPGs.csv', 'w' ) as f:
                f.write(csv_output)

        if "BD" in self.url:
            with open('Bridge Domains/CSV/Bridge Domains.csv', 'w' ) as f:
                f.write(csv_output)

        if "Ctx" in self.url:
            with open('Contexts/CSV/Contexts.csv', 'w' ) as f:
                f.write(csv_output)

        if "Ap" in self.url:
            with open('Application Profiles/CSV/Application Profiles.csv', 'w' ) as f:
                f.write(csv_output)

        if "l3extOut" in self.url:
            with open('L3Outs/CSV/L3Outs.csv', 'w' ) as f:
                f.write(csv_output)

        if "topSystem" in self.url:
            with open('Top System/CSV/Top System.csv', 'w' ) as f:
                f.write(csv_output)

        if "Subnet" in self.url:
            with open('Subnets/CSV/Subnets.csv', 'w' ) as f:
                f.write(csv_output)

        if "CEp" in self.url:
            with open('Endpoints/CSV/Endpoints.csv', 'w' ) as f:
                f.write(csv_output)

    def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        markdown_template = env.get_template('aci_markdown.j2')      
        markdown_output = markdown_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json),
                                         url = self.aci)
        if "Tenant" in self.url:                                         
            with open('Tenant/Markdown/Tenants.md', 'w' ) as f:
                f.write(markdown_output)

        if "AEPg" in self.url:
            with open('EPG/Markdown/EPGs.md', 'w' ) as f:
                f.write(markdown_output)

        if "BD" in self.url:
            with open('Bridge Domains/Markdown/Bridge Domains.md', 'w' ) as f:
                f.write(markdown_output)

        if "Ctx" in self.url:
            with open('Contexts/Markdown/Contexts.md', 'w' ) as f:
                f.write(markdown_output)

        if "Ap" in self.url:
            with open('Application Profiles/Markdown/Application Profiles.md', 'w' ) as f:
                f.write(markdown_output)

        if "l3extOut" in self.url:
            with open('L3Outs/Markdown/L3Outs.md', 'w' ) as f:
                f.write(markdown_output)

        if "topSystem" in self.url:
            with open('Top System/Markdown/Top System.md', 'w' ) as f:
                f.write(markdown_output)

        if "Subnet" in self.url:
            with open('Subnets/Markdown/Subnets.md', 'w' ) as f:
                f.write(markdown_output)

        if "CEp" in self.url:
            with open('Endpoints/Markdown/Endpoints.md', 'w' ) as f:
                f.write(markdown_output)

    def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        html_template = env.get_template('aci_html.j2')      
        html_output = html_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json),
                                         url = self.aci)
        if "Tenant" in self.url:                                         
            with open('Tenant/HTML/Tenants.html', 'w' ) as f:
                f.write(html_output)

        if "AEPg" in self.url:
            with open('EPG/HTML/EPGs.html', 'w' ) as f:
                f.write(html_output)

        if "BD" in self.url:
            with open('Bridge Domains/HTML/Bridge Domains.html', 'w' ) as f:
                f.write(html_output)

        if "Ctx" in self.url:
            with open('Contexts/HTML/Contexts.html', 'w' ) as f:
                f.write(html_output)

        if "Ap" in self.url:
            with open('Application Profiles/HTML/Application Profiles.html', 'w' ) as f:
                f.write(html_output)

        if "l3extOut" in self.url:
            with open('L3Outs/HTML/L3Outs.html', 'w' ) as f:
                f.write(html_output)

        if "topSystem" in self.url:
            with open('Top System/HTML/Top System.html', 'w' ) as f:
                f.write(html_output)

        if "Subnet" in self.url:
            with open('Subnets/HTML/Subnets.html', 'w' ) as f:
                f.write(html_output)

        if "CEp" in self.url:
            with open('Endpoints/HTML/Endpoints.html', 'w' ) as f:
                f.write(html_output)

    def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        mindmap_template = env.get_template('aci_mindmap.j2')      
        mindmap_output = mindmap_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json),
                                         url = self.aci)
        if "Tenant" in self.url:                                         
            with open('Tenant/Mindmap/Tenants.md', 'w' ) as f:
                f.write(mindmap_output)

        if "AEPg" in self.url:
            with open('EPG/Mindmap/EPGs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "BD" in self.url:
            with open('Bridge Domains/Mindmap/Bridge Domains.md', 'w' ) as f:
                f.write(mindmap_output)

        if "Ctx" in self.url:
            with open('Contexts/Mindmap/Contexts.md', 'w' ) as f:
                f.write(mindmap_output)

        if "Ap" in self.url:
            with open('Application Profiles/Mindmap/Application Profiles.md', 'w' ) as f:
                f.write(mindmap_output)

        if "l3extOut" in self.url:
            with open('L3Outs/Mindmap/L3Outs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "topSystem" in self.url:
            with open('Top System/Mindmap/Top System.md', 'w' ) as f:
                f.write(mindmap_output)

        if "Subnet" in self.url:
            with open('Subnets/Mindmap/Subnets.md', 'w' ) as f:
                f.write(mindmap_output)

        if "CEp" in self.url:
            with open('Endpoints/Mindmap/Endpoints.md', 'w' ) as f:
                f.write(mindmap_output)

    def all_files(self, parsed_json):
        self.json_file(parsed_json)
        self.yaml_file(parsed_json)
        self.csv_file(parsed_json)
        self.markdown_file(parsed_json)
        self.html_file(parsed_json)
        self.mindmap_file(parsed_json)
        
@click.command()
@click.option('--url',
    prompt="APIC URL",
    help="APIC URL",
    required=True,envvar="URL")
@click.option('--username',
    prompt="APIC Username",
    help="APIC Username",
    required=True,envvar="USERNAME")
@click.option('--password',
    prompt="APIC Password",
    help="APIC Password",
    required=True, hide_input=True,envvar="PASSWORD")
def cli(url,username,password):
    invoke_class = ACEye(url,username,password)
    invoke_class.aceye()

if __name__ == "__main__":
    cli()
