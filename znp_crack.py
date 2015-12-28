from tools import rand, pow_mod, gcd
from requests import get

base_url = "http://asymcryptwebservice.appspot.com/znp/"
key_size = 2048

response = get(base_url+"serverKey")
cookies = response.cookies
n = response.json()["modulus"]
n = int(n, 16)

print "Received key: %X" % (n)

attempts = 1
while True:
    print "Attempt", attempts
    attempts += 1

    t = rand(key_size)
    y = pow_mod(t, 2, n)

    payload = {"y": "%X" % (y)}
    response = get(base_url+"challenge", payload, cookies=cookies).json()
    root = response["root"]
    root = int(root, 16)

    print "t = %X" % (t)
    print "y = %X" % (y)
    print "root = %X" % (root)

    if root != t:
        p = gcd(t + root, n)
        q = n / p

        print "Success."
        print "p: %X" % (p)
        print "q: %X" % (q)
        print "p*q == n:", p*q == n
        break
    else:
        print "Fail."
