# Elite v1.1.1

```

```py
import elite
# server side
s = elite.getscheme()
# client side
c = elite.getscheme()
```

After instantiating a scheme, you can export your local public key or import remote key by calling the following methods:
```py
# binary version
c.importBinaryKey(s.exportBinaryKey())
# hex version
s.importHexKey(c.exportHexKey())

# should be the same
print(s.secret())
print(c.secret())

data = s.encrypt(b'data')
assert b'data' == c.decrypt(data)


from elite.scheme import P384r1AesGcmScheme
# secp384r1 with AES_GCM
s = P384r1AesGcmScheme()
c = P384r1AesGcmScheme()

from elite.scheme import ECCScheme
from elite.cipher import getprovider
from elite.secret import CurveKind

s = ECCScheme(CurveKind.CK_SECP256K1, getprovider())

