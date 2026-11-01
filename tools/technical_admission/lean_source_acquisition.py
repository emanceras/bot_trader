"""Acquire one pinned blobless LEAN commit under a conservative TLS byte cap.

This is an installation helper, not an engine adapter. No checkout or dataset
body is requested. The CONNECT proxy preserves Git's HTTPS certificate checking.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import http.server
import json
import os
from pathlib import Path
import select
import socket
import socketserver
import subprocess
import threading
import time
import urllib.parse
import urllib.request

ROOT = Path('/workspace/technical-admission/E')
COMMIT = '22404ea28b8d3f3c9eb74d6ed9f0444426f8e417'
URL = 'https://github.com/QuantConnect/Lean.git'
MAXIMUM = 100 * 1024**2


def append(row):
    with (ROOT/'downloads.jsonl').open('a') as f:
        f.write(json.dumps(row,sort_keys=True)+'\n')
        f.flush(); os.fsync(f.fileno())


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--checkout-plan',type=Path)
    args=parser.parse_args()
    started = time.monotonic()
    used = sum(json.loads(line).get('body_bytes',0) for line in (ROOT/'downloads.jsonl').read_text().splitlines())
    if used+MAXIMUM+32768 > 2*1024**3:
        raise RuntimeError('insufficient E transfer allowance')
    repository=ROOT/'lean-source'
    paths=[]
    if args.checkout_plan:
        plan=json.loads(args.checkout_plan.read_text())
        if plan['commit']!=COMMIT or not repository.exists():
            raise RuntimeError('missing pinned repository or wrong plan')
        paths=plan['paths']
        forbidden={'Data','Tests','Algorithm.Python','Launcher','DownloaderDataProvider','ToolBox','Report','Research','Optimizer','Optimizer.Launcher'}
        for path in paths:
            parts=Path(path).parts
            if not parts or parts[0] in forbidden or '..' in parts or Path(path).is_absolute():
                raise RuntimeError('excluded checkout path')
            if not (path.endswith(('.cs','.csproj','.props','.targets','.resx','.py')) or path in ('LICENSE','NOTICE','.nuget/NuGet.config')):
                raise RuntimeError('non-source checkout body excluded')
    else:
        request=urllib.request.Request(URL+'/info/refs?service=git-upload-pack',headers={'Git-Protocol':'version=2','User-Agent':'bot-trader-authorized-technical-audit/1'})
        with urllib.request.urlopen(request,timeout=30) as response:
            payload=response.read(32768)
            if len(payload)==32768:
                raise RuntimeError('capability response exceeds metadata bound')
        (ROOT/'lean-capabilities.bin').write_bytes(payload)
        append({'url':request.full_url,'body_bytes':len(payload),'status':'capability_probe','sha256':hashlib.sha256(payload).hexdigest(),'wall_seconds':time.monotonic()-started})
        if b'filter' not in payload or b'fetch=' not in payload:
            raise RuntimeError('server does not advertise v2 fetch filtering; no fallback')
        if repository.exists():
            raise RuntimeError('source directory already exists; no silent retry')
    env=os.environ.copy()
    env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_TERMINAL_PROMPT='0',GIT_LFS_SKIP_SMUDGE='1',GIT_ALLOW_PROTOCOL='https')
    if not args.checkout_plan:
        subprocess.run(['git','init',str(repository)],check=True,env=env)
    upstream=urllib.parse.urlsplit(os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or '')
    count=0
    lock=threading.Lock()
    connections=[]
    errors=[]
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self,*_args):
            pass
        def do_CONNECT(self):
            nonlocal count
            if self.path!='github.com:443':
                self.send_error(403); return
            try:
                if upstream.hostname:
                    if upstream.scheme!='http':
                        raise RuntimeError('unsupported upstream proxy transport')
                    peer=socket.create_connection((upstream.hostname,upstream.port or 80),timeout=30)
                    auth=''
                    if upstream.username:
                        raw=f'{urllib.parse.unquote(upstream.username)}:{urllib.parse.unquote(upstream.password or "")}'.encode()
                        auth='Proxy-Authorization: Basic '+base64.b64encode(raw).decode()+'\r\n'
                    peer.sendall(('CONNECT github.com:443 HTTP/1.1\r\nHost: github.com:443\r\n'+auth+'\r\n').encode())
                    reply=b''
                    while not reply.endswith(b'\r\n\r\n') and len(reply)<8192:
                        reply+=peer.recv(1)
                    if b' 200 ' not in reply.split(b'\r\n',1)[0]:
                        raise RuntimeError('upstream CONNECT rejected')
                else:
                    peer=socket.create_connection(('github.com',443),timeout=30)
                connections.append(peer)
                self.send_response(200,'Connection established'); self.end_headers()
                self.connection.settimeout(30); peer.settimeout(30)
                while True:
                    ready,_,_=select.select([self.connection,peer],[],[],30)
                    if not ready:
                        raise TimeoutError('Git proxy idle timeout')
                    for source in ready:
                        with lock:
                            left=MAXIMUM-count
                            if left<=0:
                                raise RuntimeError('conservative transfer ceiling reached')
                            data=source.recv(min(16384,left))
                            count+=len(data)
                        if not data:
                            return
                        (peer if source is self.connection else self.connection).sendall(data)
            except Exception as exc:
                errors.append(type(exc).__name__+': '+str(exc))
            finally:
                if 'peer' in locals():
                    peer.close()
    class Server(socketserver.ThreadingMixIn,http.server.HTTPServer):
        daemon_threads=True
    server=Server(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    started=time.monotonic()
    status='blocked'
    try:
        address=f'http://127.0.0.1:{server.server_port}'
        common=['git','-C',str(repository),'-c','http.proxy='+address,'-c','protocol.version=2','-c','fetch.recurseSubmodules=false']
        if args.checkout_plan:
            subprocess.run(common+['sparse-checkout','init','--no-cone'],check=True,env=env)
            subprocess.run(common+['sparse-checkout','set','--no-cone','--stdin'],input=''.join('/'+p+'\n' for p in paths),text=True,check=True,env=env)
            command=common+['checkout','--detach',COMMIT]
        else:
            command=common+['fetch','--no-tags','--depth=1','--filter=blob:none',URL,COMMIT]
        result=subprocess.run(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
        label=args.checkout_plan.stem if args.checkout_plan else 'lean-fetch'
        (ROOT/(label+'-output.log')).write_bytes(result.stdout)
        print(result.stdout.decode(errors='replace'))
        if result.returncode:
            raise RuntimeError(f'pinned partial fetch failed exit={result.returncode}')
        if b'filtering not recognized' in result.stdout.lower():
            raise RuntimeError('server ignored filter; stop source route')
        actual=subprocess.check_output(['git','-C',str(repository),'rev-parse','HEAD' if args.checkout_plan else 'FETCH_HEAD'],env=env,text=True).strip()
        if actual!=COMMIT:
            raise RuntimeError('pinned commit identity mismatch')
        # Disable lazy fetching while auditing the fetched object kinds.
        inspect_env={**env,'GIT_NO_LAZY_FETCH':'1'}
        kinds=subprocess.check_output(['git','-C',str(repository),'cat-file','--batch-all-objects','--batch-check=%(objecttype)'],env=inspect_env,text=True).splitlines()
        if not args.checkout_plan:
            if 'blob' in kinds:
                raise RuntimeError('unexpected blob bodies in initial blobless fetch')
            inventory=subprocess.check_output(['git','-C',str(repository),'ls-tree','-r',COMMIT],env=inspect_env)
            (ROOT/'lean-tree.txt').write_bytes(inventory)
            status='verified_blobless_commit'
            print(json.dumps({'commit':actual,'objects':len(kinds),'blob_bodies':0,'tree_entries':len(inventory.splitlines())}))
        else:
            actual_paths=sorted(str(p.relative_to(repository)) for p in repository.rglob('*') if p.is_file() and '.git' not in p.relative_to(repository).parts)
            if actual_paths!=sorted(paths):
                raise RuntimeError('checkout file set differs from exact source allowlist')
            manifest={p:hashlib.sha256((repository/p).read_bytes()).hexdigest() for p in actual_paths}
            (ROOT/(args.checkout_plan.stem+'-manifest.json')).write_text(json.dumps({'commit':COMMIT,'sha256':manifest},indent=2)+'\n')
            status='verified_sparse_source_checkout'
            print(json.dumps({'commit':COMMIT,'source_files':len(actual_paths),'blobs_total':kinds.count('blob'),'financial_data_files':0}))
    finally:
        server.shutdown(); server.server_close()
        for peer in connections:
            try: peer.close()
            except OSError: pass
        append({'url':URL,'body_bytes':count,'measurement':'conservative upper bound: TLS tunnel bytes in both directions, not exact HTTP response body bytes','status':status,'commit':COMMIT,'maximum_bytes':MAXIMUM,'checkout_plan':str(args.checkout_plan) if args.checkout_plan else None,'proxy_errors':errors,'wall_seconds':time.monotonic()-started})
    return 0

if __name__=='__main__':
    raise SystemExit(main())
