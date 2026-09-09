import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2 import VpcClient
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v2.model import CreateSecurityGroupRuleRequest, CreateSecurityGroupRuleRequestBody, SecurityGroupRule

def configure_rules():
    # Authenticate using your existing environment variables
    ak = os.getenv("HUAWEICLOUD_SDK_AK")
    sk = os.getenv("HUAWEICLOUD_SDK_SK")
    credentials = BasicCredentials(ak, sk)
    
    client = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(VpcRegion.value_of("af-south-1")) \
        .build()

    # The specific Security Group ID generated in your previous step
    target_sg_id = "af090e9c-6648-4e21-a7a5-fc24ca06273f"
    print(f"Injecting rules into Security Group: {target_sg_id}")

    # Rule 1: Allow SSH (Port 22)
    ssh_rule = SecurityGroupRule(
        security_group_id=target_sg_id,
        direction="ingress",
        ethertype="IPv4",
        protocol="tcp",
        port_range_min=22,
        port_range_max=22,
        remote_ip_prefix="0.0.0.0/0",
        description="EMSI NetDevOps - Allow SSH"
    )
    client.create_security_group_rule(
        CreateSecurityGroupRuleRequest(body=CreateSecurityGroupRuleRequestBody(security_group_rule=ssh_rule))
    )
    print("- SSH (Port 22) Rule Active")

    # Rule 2: Allow HTTP (Port 80)
    http_rule = SecurityGroupRule(
        security_group_id=target_sg_id,
        direction="ingress",
        ethertype="IPv4",
        protocol="tcp",
        port_range_min=80,
        port_range_max=80,
        remote_ip_prefix="0.0.0.0/0",
        description="EMSI NetDevOps - Allow HTTP"
    )
    client.create_security_group_rule(
        CreateSecurityGroupRuleRequest(body=CreateSecurityGroupRuleRequestBody(security_group_rule=http_rule))
    )
    print("- HTTP (Port 80) Rule Active")
    print("Firewall simulation complete.")

if __name__ == "__main__":
    configure_rules()