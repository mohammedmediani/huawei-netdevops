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
import sys
import yaml
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2 import VpcClient
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v2.model import (
    CreateSecurityGroupRuleRequest,
    CreateSecurityGroupRuleRequestBody,
    SecurityGroupRule,
)


def load_config(filepath="network_config.yaml"):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)


def validate_credentials():
    """Pre-flight check: ensure AK/SK are present and non-empty."""
    ak = (os.getenv("HUAWEICLOUD_SDK_AK") or "").strip()
    sk = (os.getenv("HUAWEICLOUD_SDK_SK") or "").strip()

    missing = []
    if not ak:
        missing.append("HUAWEICLOUD_SDK_AK")
    if not sk:
        missing.append("HUAWEICLOUD_SDK_SK")

    if missing:
        print("❌ Pre-flight FAILED — missing or empty credentials:")
        for var in missing:
            print(f"   • {var} is not set in the runner environment")
        print()
        print("   Fix: Add the secrets under your GitHub repo:")
        print("   Settings → Secrets and variables → Actions → New repository secret")
        sys.exit(1)

    print("✅ Pre-flight passed: AK/SK credentials are present.")
    return ak, sk


def inject_rules():
    ak, sk = validate_credentials()
    config = load_config()

    credentials = BasicCredentials(ak, sk)

    client = (
        VpcClient.new_builder()
        .with_credentials(credentials)
        .with_region(VpcRegion.value_of("af-south-1"))
        .build()
    )

    # Target Security Group ID
    target_sg_id = "9502086e-456e-4d47-8d03-f53f3d35be29"

    sg_name = config["security_group"]["name"]
    vpc_name = config["vpc"]["name"]
    rules = config["security_group"]["inbound_rules"]

    print(f"VPC Target      : {vpc_name} ({config['vpc']['cidr']})")
    print(f"Security Group  : {sg_name}")
    print(f"Region          : af-south-1")
    print(f"Injecting {len(rules)} inbound rules from network_config.yaml...")

    for rule in rules:
        sg_rule = SecurityGroupRule(
            security_group_id=target_sg_id,
            direction="ingress",
            ethertype="IPv4",
            protocol=rule["protocol"],
            port_range_min=rule["port"],
            port_range_max=rule["port"],
            remote_ip_prefix="0.0.0.0/0",
            description=rule["description"],
        )
        client.create_security_group_rule(
            CreateSecurityGroupRuleRequest(
                body=CreateSecurityGroupRuleRequestBody(security_group_rule=sg_rule)
            )
        )
        print(f"  ✓ Port {rule['port']:>4} ({rule['protocol'].upper()}) — {rule['description']}")

    print(f"\nDeployment complete. {len(rules)} rules active on '{sg_name}'.")


if __name__ == "__main__":
    inject_rules()