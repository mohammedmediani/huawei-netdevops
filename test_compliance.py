"""
test_compliance.py
-------------------
NetDevOps DevSecOps Compliance Audit

Queries the live Huawei Cloud Security Group rules and asserts:
  - Required ports (22, 80, 443) are OPEN on ingress
  - Unsafe port (23/Telnet) is BLOCKED
"""

import os
import sys
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2 import VpcClient
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v2.model import ListSecurityGroupRulesRequest


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


def test_compliance():
    ak, sk = validate_credentials()

    credentials = BasicCredentials(ak, sk)

    client = (
        VpcClient.new_builder()
        .with_credentials(credentials)
        .with_region(VpcRegion.value_of("af-south-1"))
        .build()
    )

    # Target Security Group ID
    target_sg_id = "9502086e-456e-4d47-8d03-f53f3d35be29"

    print("Running DevSecOps Compliance Audit...")
    response = client.list_security_group_rules(
        ListSecurityGroupRulesRequest(security_group_id=target_sg_id)
    )

    active_ports = [
        rule.port_range_min
        for rule in response.security_group_rules
        if rule.direction == "ingress"
    ]

    assert 22 in active_ports, "FAIL: SSH (Port 22) is missing."
    assert 80 in active_ports, "FAIL: HTTP (Port 80) is missing."
    assert 443 in active_ports, "FAIL: HTTPS (Port 443) is missing."
    assert 23 not in active_ports, "CRITICAL: Insecure Telnet (Port 23) is exposed."

    print("✅ Audit Passed: Firewall rules comply with EMSI/Huawei enterprise policies.")
    print("   - Port 22  (SSH)   : OPEN   ✓")
    print("   - Port 80  (HTTP)  : OPEN   ✓")
    print("   - Port 443 (HTTPS) : OPEN   ✓")
    print("   - Port 23  (Telnet): BLOCKED ✓")


if __name__ == "__main__":
    test_compliance()