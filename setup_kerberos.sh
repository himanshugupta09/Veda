#!/bin/bash
# Predefine debconf responses to suppress interactive prompts
export DEBIAN_FRONTEND=noninteractive

# Install dependencies without prompts
apt-get update && apt-get install -y krb5-user

echo -e "[libdefaults]\ndefault_realm = vedji.COM" > /etc/krb5.conf
