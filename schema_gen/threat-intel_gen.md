<!-- Generated from schema\threat-intel.jadn, Wed Mar  7 15:19:46 2018-->
<!--
-->

# Threat Intelligence Actuator Profile
## Module tint, version 0.1
Datatypes used to support the Set Reputation use case.
## 3.2 Structure Types
### 3.2.1 Reputation
Information about the reputation of an entity.

| |Record| | | |
|---:|---|---|---:|---|
|**ID**|**Name**|**Type**|**#**|**Description**|
|1|type|rep-type|1|The type of object for which the reputation should be set.|
|2|name|String|1|The name of the file or domain.|
|3|severity|rep-score|1|Score from 0-7, with 0 being trusted and 7 being known bad.|
|4|comment|String|0..1|Comment of justification as to why this was set.|
|5|hashes|hashes|0..n|Hashes of some data about the entity(ies).|
|6|ips|ip-addr|0..n|List of IP addresses.|
### 3.2.2 Device


| |Map| | | |
|---:|---|---|---:|---|
|**ID**|**Name**|**Type**|**#**|**Description**|
|1|hostname|hostname|1|The hostname of device|
|2|ipv4_addr|ipv4-addr|0..1|The IPv4 address of a device.|
|5|ipv6_addr|ipv6-addr|0..1|The IPv6 address of a device.|
|6|id|String|1|The registered device ID.|
### 3.3.3 rep-type


|ID|Name|Description|
|---:|---|---|
|0|file|Reputation applies to a file object.|
|1|domain|Reputation applies to a domain object.|
### 3.2.4 hashes
Hash values

| |Map| | | |
|---:|---|---|---:|---|
|**ID**|**Name**|**Type**|**#**|**Description**|
|1|MD5|Binary|0..1|MD5 message digest as defined in RFC3121|
|4|SHA-1|Binary|0..1|Secure Hash Algorithm (SHA)-1 as defined in RFC3174|
|5|SHA-224|Binary|0..1|SHA-224 as defined in RFC6234 (US Secure Hash Algorithms)|
|7|SHA-384|Binary|0..1|SHA-384 as defined in RFC6234|
|9|SHA3-224|Binary|0..1|SHA3-224 as defined in FIPS PUP 202|
|12|SHA3-512|Binary|0..1|SHA3-512 as defined in FIPS PUP 202|
### 3.3.5 rep-score


|Value|Description|
|---|---|
|0|Not Set|
|1|Benign|
|2|Likely Benign|
|3|Possibly Benign|
|4|Indeterminate|
|5|Possibly Malicious|
|6|Likely Malicious|
|7|Known Malicious|
## 3.3 Primitive Types
|Name|Type|Description|
|---|---|---|
|ip-addr|String (ip)|IPv4 or IPv6 address|
|hostname|String (hostname)|Domain name, RFC 1034, section 3.5|
|ipv4-addr|String (ipv4)|IPv4 address or range in CIDR notation, RFC 2673, section 3.2|
|ipv6-addr|String (ipv6)|IPv6 address or range, RFC 4291, section 2.2|
