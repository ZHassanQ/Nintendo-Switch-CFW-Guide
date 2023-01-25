#!/usr/bin/python3
import sys
try:
    from dns import resolver  # dnspython
except ModuleNotFoundError:
    print("You need dnspython to use this script.")
    print("Run 'pip install dnspython' to install it.")
    sys.exit()

print("90DNS Tester by aveao/AveSatanas, released under GPLv2.")

# Initialize resolver, set up the DNS servers
dns_resolver = resolver.Resolver()
dns_resolver.nameservers = ['163.172.141.219', '207.246.121.77']

# Define a basic dataset, with a list of the most important domains
# Yes, I know that this is ugly, but I wrote it on 8AM after a sleepless night
test_dataset = [['nintendo.net', ['127.0.0.1']],
                ['sun.hac.lp1.d4c.nintendo.net', ['127.0.0.1']],
                ['nintendo.com', ['127.0.0.1']],
                ['ctest.cdn.nintendo.net', ['207.246.121.77', '95.216.149.205']],
                ['conntest.nintendowifi.net',
                 ['207.246.121.77', '95.216.149.205']],
                ['90dns.test', ['207.246.121.77', '95.216.149.205']],
                ]


def compare_dns(domain_to_test, expected_ips):
    # Query a domain's A records, convert first result to string
    # and check if it's in the list of expected IPs
    try:
        return (str(dns_resolver.query(domain_to_test, 'A')[0]) in expected_ips)
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        # No answer or no domain, fail
        return ""


print("Starting tests now.\n")

test_successes = 0
for test_data in test_dataset:
    if not (compare_dns(test_data[0], test_data[1])):
        # fstrings are good and all, but I wanted to support py2
        print("Incorrect records detected on {}.".format(test_data[0]))
    else:
        test_successes += 1
        print("All good on {}.".format(test_data[0]))

print("\n{}/{} queries had the expected result.".format(test_successes,
                                                        len(test_dataset)))

# If all tests succeeded, notify user of that.
if test_successes == len(test_dataset):
    print("It should be safe to use 90DNS on this network.")
else:
    print("It is NOT safe to use 90DNS on this network.")
    print("Try setting up your own 90DNS instance:")
    print("https://gitlab.com/aoz/90dns/blob/master/SELFHOST.md")
