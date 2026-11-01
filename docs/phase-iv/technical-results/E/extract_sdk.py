import hashlib,json,tarfile
from pathlib import Path
root=Path('/workspace/technical-admission/E')
p=root/'downloads/dotnet-sdk-10.0.403-linux-x64.tar.gz'
expected='b7b3d8461cf98b07d2552ce9199702fa3ad010ac2671a5f8cd5136f7534e50f6855ba7bbb02b11494563f1d04156276a31cda1103b900e5eecd0d9473dc7b9c5'
assert hashlib.file_digest(p.open('rb'),'sha512').hexdigest()==expected
out=root/'dotnet'
out.mkdir(exist_ok=False)
with tarfile.open(p,'r:gz') as t:
    members=t.getmembers()
    assert sum(m.size for m in members)<2*1024**3
    t.extractall(out,members=members,filter='data')
print(json.dumps({'verified_sha512':expected,'files':len(members),'expanded_bytes':sum(m.size for m in members)}))
