import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2 import VpcClient, VpcRegion
from huaweicloudsdkvpc.v2.model import CreateVpcRequest, CreateVpcRequestBody, Vpc
from huaweicloudsdkvpc.v2.model import CreateSecurityGroupRequest, CreateSecurityGroupRequestBody, SecurityGroup

def deploy_architecture():
    # 1. Secure Authentication (Store these in Windows Environment Variables)
    ak = os.getenv("HUAWEICLOUD_SDK_AK")
    sk = os.getenv("HUAWEICLOUD_SDK_SK")
    credentials = BasicCredentials(ak, sk)
    
    # 2. Initialize the Network Client
    client = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(VpcRegion.value_of("af-south-1")) \
        .build()
        
    # 3. Provision the Virtual Private Cloud (VPC)
    print("Deploying EMSI NetDevOps VPC...")
    vpc_body = Vpc(name="emsi_netdevops_vpc", cidr="10.0.0.0/16")
    vpc_response = client.create_vpc(
        CreateVpcRequest(body=CreateVpcRequestBody(vpc=vpc_body))
    )
    print(f"VPC Created! ID: {vpc_response.vpc.id}")
    
    # 4. Provision the Security Group (Cloud Firewall Equivalent)
    print("Deploying Cloud Security Group...")
    sg_body = SecurityGroup(name="cloud_firewall_usg")
    sg_response = client.create_security_group(
        CreateSecurityGroupRequest(body=CreateSecurityGroupRequestBody(security_group=sg_body))
    )
    print(f"Security Group Created! ID: {sg_response.security_group.id}")

if __name__ == "__main__":
    deploy_architecture()