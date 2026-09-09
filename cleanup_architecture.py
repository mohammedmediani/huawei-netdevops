import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2 import VpcClient
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v2.model import DeleteSecurityGroupRequest, DeleteVpcRequest

def cleanup_architecture():
    # Authenticate using existing environment variables
    ak = os.getenv("HUAWEICLOUD_SDK_AK")
    sk = os.getenv("HUAWEICLOUD_SDK_SK")
    credentials = BasicCredentials(ak, sk)
    
    client = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(VpcRegion.value_of("af-south-1")) \
        .build()

    # The exact IDs generated during your deployment
    sg_id = "af090e9c-6648-4e21-a7a5-fc24ca06273f"
    vpc_id = "fbbdfd77-6e38-452c-8aae-7bd28b38e517"

    print("Initiating NetDevOps Teardown...")

    # Destroy Security Group
    client.delete_security_group(DeleteSecurityGroupRequest(security_group_id=sg_id))
    print("- Security Group Destroyed")

    # Destroy Virtual Private Cloud
    client.delete_vpc(DeleteVpcRequest(vpc_id=vpc_id))
    print("- VPC Destroyed")
    
    print("Environment successfully cleaned.")

if __name__ == "__main__":
    cleanup_architecture()