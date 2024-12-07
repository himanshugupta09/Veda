#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# Predefine realm for krb5-config
echo "krb5-config krb5-config/default_realm string EXAMPLE.COM" | debconf-set-selections

# Install Kerberos packages
apt-get update && apt-get install -y krb5-user

# Create local krb5.conf
mkdir -p ./config
cat > ./config/krb5.conf << EOL
[libdefaults]
    default_realm = EXAMPLE.COM
[realms]
    EXAMPLE.COM = {
        kdc = kerberos.example.com
    }
[domain_realm]
    .example.com = EXAMPLE.COM
    example.com = EXAMPLE.COM
EOL
