"""One bounded, exact-source NuGet restore; no default LEAN launcher execution."""
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
import xml.etree.ElementTree as ET

ROOT=Path('/workspace/technical-admission/E')
MAXIMUM=1024**3
HOSTS={'api.nuget.org:443','globalcdn.nuget.org:443','www.nuget.org:443'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--attempt',required=True)
    args=parser.parse_args()
    if not args.attempt.replace('-','').isalnum():
        raise ValueError('invalid attempt label')
    output=ROOT/f'lean-restore-{args.attempt}-output.log'
    resolved=ROOT/f'lean-resolved-{args.attempt}-packages.json'
    if output.exists() or resolved.exists():
        raise RuntimeError('refuse to overwrite prior attempt')
    for name in ('runtime','xdg-data'):
        (ROOT/name).mkdir(mode=0o700,exist_ok=True)
    used=sum(json.loads(x).get('body_bytes',0) for x in (ROOT/'downloads.jsonl').read_text().splitlines())
    if used+MAXIMUM>2*1024**3:
        raise RuntimeError('insufficient conservative restore transfer reservation')
    source=ROOT/'lean-source'
    plan=json.loads((ROOT/'lean-required-source-plan.json').read_text())
    direct={}
    for project in plan['projects']:
        for package in ET.parse(source/project).findall('.//PackageReference'):
            name=package.attrib['Include']; version=package.attrib['Version']
            if any(c in version for c in '*[],()$'):
                raise RuntimeError('nonfixed package reference')
            if name in direct and direct[name]!=version:
                raise RuntimeError('inconsistent direct package versions')
            direct[name]=version
    direct_path=ROOT/'lean-direct-packages.json'
    if direct_path.exists():
        if json.loads(direct_path.read_text())!=direct:
            raise RuntimeError('direct dependency graph changed')
    else:
        direct_path.write_text(json.dumps(direct,sort_keys=True,indent=2)+'\n')
    upstream=urllib.parse.urlsplit(os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or '')
    count=0; errors=[]; connections=[]; lock=threading.Lock()
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def do_CONNECT(self):
            nonlocal count
            if self.path not in HOSTS:
                errors.append('excluded host: '+self.path); self.send_error(403); return
            try:
                if upstream.hostname:
                    if upstream.scheme!='http': raise RuntimeError('unsupported upstream proxy scheme')
                    peer=socket.create_connection((upstream.hostname,upstream.port or 80),timeout=30)
                    auth=''
                    if upstream.username:
                        raw=f'{urllib.parse.unquote(upstream.username)}:{urllib.parse.unquote(upstream.password or "")}'.encode()
                        auth='Proxy-Authorization: Basic '+base64.b64encode(raw).decode()+'\r\n'
                    peer.sendall((f'CONNECT {self.path} HTTP/1.1\r\nHost: {self.path}\r\n'+auth+'\r\n').encode())
                    reply=b''
                    while not reply.endswith(b'\r\n\r\n') and len(reply)<8192: reply+=peer.recv(1)
                    if b' 200 ' not in reply.split(b'\r\n',1)[0]: raise RuntimeError('upstream CONNECT rejected')
                else:
                    host,port=self.path.split(':'); peer=socket.create_connection((host,int(port)),timeout=30)
                connections.append(peer)
                self.send_response(200,'Connection established'); self.end_headers()
                peer.settimeout(30); self.connection.settimeout(30)
                while True:
                    ready,_,_=select.select([peer,self.connection],[],[],30)
                    if not ready: raise TimeoutError('restore tunnel idle timeout')
                    for origin in ready:
                        with lock:
                            left=MAXIMUM-count
                            if left<=0: raise RuntimeError('restore transfer ceiling reached')
                            data=origin.recv(min(16384,left)); count+=len(data)
                        if not data: return
                        (self.connection if origin is peer else peer).sendall(data)
            except Exception as exc:
                errors.append(type(exc).__name__+': '+str(exc))
            finally:
                if 'peer' in locals(): peer.close()
    class Server(socketserver.ThreadingMixIn,http.server.HTTPServer): daemon_threads=True
    server=Server(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    proxy=f'http://127.0.0.1:{server.server_port}'
    env={**os.environ,'HTTP_PROXY':proxy,'HTTPS_PROXY':proxy,'http_proxy':proxy,'https_proxy':proxy,'NO_PROXY':'','no_proxy':'','NUGET_HTTP_CACHE_PATH':str(ROOT/'nuget-http-cache'),'NUGET_PLUGINS_CACHE_PATH':str(ROOT/'nuget-plugin-cache'),'NUGET_CERT_REVOCATION_MODE':'offline','DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE':'true','XDG_RUNTIME_DIR':str(ROOT/'runtime'),'XDG_DATA_HOME':str(ROOT/'xdg-data'),'DOTNET_GENERATE_ASPNET_CERTIFICATE':'false'}
    command=[str(ROOT/'dotnet/dotnet'),'restore',str(source/'Engine/QuantConnect.Lean.Engine.csproj'),'--source','https://api.nuget.org/v3/index.json','--use-lock-file','--disable-parallel','--no-http-cache','-p:NuGetAudit=false']
    start=time.monotonic(); code=None
    try:
        result=subprocess.run(command,cwd=source,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
        code=result.returncode
        output.write_bytes(result.stdout)
        print(result.stdout.decode(errors='replace'))
        locks={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source.rglob('packages.lock.json')}
        packages={str(p.relative_to(ROOT/'nuget')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'nuget').rglob('*.nupkg')}
        resolved.write_text(json.dumps({'exit_code':code,'locks_sha256':locks,'packages_sha256':packages,'command':command,'nuget_audit':'disabled for bounded setup; no vulnerability clearance claimed'},sort_keys=True,indent=2)+'\n')
        return code
    finally:
        server.shutdown(); server.server_close()
        for peer in connections:
            try: peer.close()
            except OSError: pass
        row={'url':'https://api.nuget.org/v3/index.json','attempt':args.attempt,'body_bytes':count,'measurement':'conservative upper bound: TLS tunnel bytes in both directions, not exact HTTP response bodies','maximum_bytes':MAXIMUM,'status':'restore_succeeded' if code==0 else 'restore_blocked','exit_code':code,'proxy_errors':errors,'wall_seconds':time.monotonic()-start}
        with (ROOT/'downloads.jsonl').open('a') as f:
            f.write(json.dumps(row,sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())

if __name__=='__main__': raise SystemExit(main())
