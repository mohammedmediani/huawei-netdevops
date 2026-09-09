"""
deploy_yaml_architecture.py
----------------------------
NetDevOps Phase 2 — YAML-Driven Security Group Rule Injection

Reads firewall rules from network_config.yaml and injects them into
the target Security Group in the Huawei Cloud af-south-1 region.
Credentials are sourced exclusively from environment variables:
  HUAWEICLOUD_SDK_AK  —  Access Key
  HUAWEICLOUD_SDK_SK  —  Secret Key
"""

import os
import yaml
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2 import VpcClient
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v2.model import CreateSecurityGroupRuleRequest, CreateSecurityGroupRuleRequestBody, SecurityGroupRule

def load_config(filepath="network_config.yaml"):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def inject_rules():
    config = load_config()
    ak = os.getenv("HUAWEICLOUD_SDK_AK")
    sk = os.getenv("HUAWEICLOUD_SDK_SK")
    credentials = BasicCredentials(ak, sk)
    
    client = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(VpcRegion.value_of("af-south-1")) \
        .build()

    # Your newly generated Security Group ID
    target_sg_id = "9502086e-456e-4d47-8d03-f53f3d35be29"
    
    sg_name = config['security_group']['name']
    vpc_name = config['vpc']['name']
    rules = config['security_group']['inbound_rules']
    print(f"VPC Target      : {vpc_name} ({config['vpc']['cidr']})")
    print(f"Security Group  : {sg_name}")
    print(f"Region          : af-south-1")
    print(f"Injecting {len(rules)} inbound rules from network_config.yaml...")
    
    for rule in rules:
        sg_rule = SecurityGroupRule(
            security_group_id=target_sg_id,
            direction="ingress",
            ethertype="IPv4",
            protocol=rule['protocol'],
            port_range_min=rule['port'],
            port_range_max=rule['port'],
            remote_ip_prefix="0.0.0.0/0",
            description=rule['description']
        )
        client.create_security_group_rule(
            CreateSecurityGroupRuleRequest(body=CreateSecurityGroupRuleRequestBody(security_group_rule=sg_rule))
        )
        print(f"  ✓ Port {rule['port']:>4} ({rule['protocol'].upper()}) — {rule['description']}")

    print(f"\nDeployment complete. {len(rules)} rules active on '{sg_name}'.")

if __name__ == "__main__":
    inject_rules()