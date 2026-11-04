"""Bounded offline subprocesses and verified downloads for authorized M/R/E QA."""
from __future__ import annotations

import argparse
import ctypes
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = Path('/workspace/technical-admission')
GIB = 1024**3
LIMITS = {'M': (2, 4*GIB, 3*GIB, 512*1024**2, 7200),
          'R': (1, GIB, GIB//2, 0, 3600),
          'E': (4, 8*GIB, 8*GIB, 2*GIB, 14400)}

def append(path, value):
    with path.open('a') as f:
        f.write(json.dumps(value, sort_keys=True)+'\n')
        f.flush()
        os.fsync(f.fileno())

def rows(path):
    return [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []

def size(path):
    total = 0
    for base, _, names in os.walk(path):
        for name in names:
            try:
                p = Path(base)/name
                if not p.is_symlink():
                    total += p.stat().st_size
            except FileNotFoundError:
                pass
    return total

def restrict(root: Path, network: bool):
    """Use available Landlock; always deny IPv4/IPv6 sockets for offline runs."""
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(38, 1, 0, 0, 0):
        raise OSError(ctypes.get_errno(), 'no_new_privs')
    abi = libc.syscall(444, 0, 0, 1)
    if abi >= 3:
        class Ruleset(ctypes.Structure):
            _fields_ = [('handled_access_fs', ctypes.c_uint64)]
        class Beneath(ctypes.Structure):
            _pack_ = 1
            _fields_ = [('allowed_access', ctypes.c_uint64), ('parent_fd', ctypes.c_int32)]
        access = sum(1 << bit for bit in [1,4,5,6,7,8,9,10,11,12,13,14])
        rule = Ruleset(access)
        fd = libc.syscall(444, ctypes.byref(rule), ctypes.sizeof(rule), 0)
        if fd < 0:
            raise OSError(ctypes.get_errno(), 'landlock_create')
        for path, allowed in [(root, access), (Path('/dev/null'), 1 << 1)]:
            pfd = os.open(path, os.O_PATH | os.O_CLOEXEC)
            item = Beneath(allowed, pfd)
            if libc.syscall(445, fd, 1, ctypes.byref(item), 0):
                raise OSError(ctypes.get_errno(), f'landlock_add:{path}')
            os.close(pfd)
        if libc.syscall(446, fd, 0):
            raise OSError(ctypes.get_errno(), 'landlock_restrict')
        os.close(fd)
    if not network:
        sec = ctypes.CDLL('libseccomp.so.2', use_errno=True)
        sec.seccomp_init.argtypes = [ctypes.c_uint32]
        sec.seccomp_init.restype = ctypes.c_void_p
        sec.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
        sec.seccomp_syscall_resolve_name.restype = ctypes.c_int
        class Compare(ctypes.Structure):
            _fields_ = [('arg',ctypes.c_uint),('op',ctypes.c_int),
                        ('a',ctypes.c_uint64),('b',ctypes.c_uint64)]
        sec.seccomp_rule_add_array.argtypes = [ctypes.c_void_p,ctypes.c_uint32,
                                              ctypes.c_int,ctypes.c_uint,ctypes.POINTER(Compare)]
        sec.seccomp_load.argtypes = [ctypes.c_void_p]
        sec.seccomp_release.argtypes = [ctypes.c_void_p]
        ctx = sec.seccomp_init(0x7fff0000)
        for domain in (2, 10):
            comparison = Compare(0,4,domain,0)
            result = sec.seccomp_rule_add_array(ctx, 0x00050000 | errno.EPERM,
                sec.seccomp_syscall_resolve_name(b'socket'),1,ctypes.byref(comparison))
            if result:
                raise RuntimeError(f'seccomp rule error {result}')
        if sec.seccomp_load(ctx):
            raise RuntimeError('seccomp_load failed')
        sec.seccomp_release(ctx)

def group_rss(pgid):
    total = 0
    for path in Path('/proc').glob('[0-9]*/stat'):
        try:
            values = path.read_text().rsplit(')',1)[1].split()
            if int(values[2]) == pgid:
                total += int(values[21])*os.sysconf('SC_PAGE_SIZE')
        except (OSError,ValueError,IndexError):
            pass
    return total

def run(args):
    package = ROOT/args.package
    cpus, memory, disk, _, seconds = LIMITS[args.package]
    elapsed = sum(x.get('wall_seconds',0) for x in rows(package/'runs.jsonl') + rows(package/'downloads.jsonl'))
    allowance = min(args.seconds or seconds, seconds-elapsed)
    if allowance <= 0 or size(package) >= disk or size(ROOT) >= 12*GIB:
        raise RuntimeError('resource envelope exhausted before launch')
    if (package/f'{args.label}.log').exists():
        raise RuntimeError('attempt label already exists; no overwrite')
    env = os.environ.copy()
    env.update({'TMPDIR':str(package/'tmp'),'PYTHONDONTWRITEBYTECODE':'1',
                'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1',
                'NUMEXPR_NUM_THREADS':'1','RAYON_NUM_THREADS':str(cpus),
                'UV_CACHE_DIR':str(package/'uv-cache'),
                'UV_PYTHON_INSTALL_DIR':str(package/'python'),
                'DOTNET_CLI_HOME':str(package/'dotnet-home'),
                'DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1',
                'NUGET_PACKAGES':str(package/'nuget')})
    cmd = args.command[1:] if args.command[:1] == ['--'] else args.command
    bootstrap = [sys.executable,str(Path(__file__).resolve()),'child']
    if args.network:
        bootstrap += ['--network']
    bootstrap += [args.package,'--',*cmd]
    start = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    peak = 0
    stop = None
    with (package/f'{args.label}.log').open('wb') as log:
        proc = subprocess.Popen(bootstrap,stdout=log,stderr=subprocess.STDOUT,
                                env=env,start_new_session=True,cwd=args.cwd or str(package))
        while proc.poll() is None:
            peak = max(peak,group_rss(proc.pid))
            if peak > memory*0.90:
                stop = 'memory_guard_band'
            if time.monotonic()-start > allowance:
                stop = 'time_limit'
            if size(package) > disk*0.95 or size(ROOT) > 12*GIB*0.95:
                stop = 'disk_guard_band'
            if stop:
                os.killpg(proc.pid,signal.SIGKILL)
                break
            time.sleep(0.1)
        code = proc.wait()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    result = {'package':args.package,'label':args.label,'command':cmd,'exit_code':code,
        'wall_seconds':time.monotonic()-start,
        'cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
        'peak_sampled_process_group_rss_bytes':peak,'scratch_bytes_after':size(package),
        'stop_reason':stop,'network_allowed':args.network,
        'isolation':'Disposable package working directory, environment and source export; original runtime integrity checked separately. Landlock unavailable on this host (ENOSYS); IPv4/IPv6 seccomp denial when offline; CPU affinity and sampled resource guard bands',
        'limits':'RSS sampled every100ms, not kernel cgroup hard limit; child thread affinity inherited; no malicious-escape certification',
        'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(time.time()-(time.monotonic()-start)))}
    append(package/'runs.jsonl',result)
    print(json.dumps(result))
    return code

def fetch(args):
    package = ROOT/args.package
    ledger = package/'downloads.jsonl'
    used = sum(x.get('body_bytes',0) for x in rows(ledger))
    cap = LIMITS[args.package][3]-used
    path = package/args.output
    if path.exists() or args.maximum > cap:
        raise RuntimeError('existing artifact or insufficient transfer budget')
    path.parent.mkdir(parents=True,exist_ok=True)
    result = {'url':args.url,'output':str(path),'body_bytes':0,'status':'started'}
    digest = hashlib.new(args.algorithm)
    start = time.monotonic()
    try:
        request = urllib.request.Request(args.url,headers={'User-Agent':'bot-trader-authorized-technical-audit/1'})
        with urllib.request.urlopen(request,timeout=30) as response:
            result.update(http_status=response.status,final_url=response.url)
            length = response.headers.get('Content-Length')
            if length and int(length) > args.maximum:
                raise RuntimeError('advertised size exceeds reserved allowance')
            with path.open('xb') as output:
                while True:
                    left = args.maximum-result['body_bytes']
                    block = response.read(min(1024*1024,left)) if left else b''
                    if not block:
                        if length and result['body_bytes'] != int(length):
                            raise RuntimeError('incomplete download')
                        break
                    result['body_bytes'] += len(block)
                    digest.update(block)
                    output.write(block)
        result['digest'] = digest.hexdigest()
        if args.expected and result['digest'] != args.expected:
            raise RuntimeError('artifact hash mismatch')
        if args.size is not None and result['body_bytes'] != args.size:
            raise RuntimeError('artifact size mismatch')
        result['status'] = 'verified'
    except Exception as exc:
        result['status'] = 'blocked'
        result['error'] = str(exc)
        if isinstance(exc,urllib.error.HTTPError):
            result['http_status'] = exc.code
    result['wall_seconds'] = time.monotonic()-start
    append(ledger,result)
    print(json.dumps(result))
    return 0 if result['status']=='verified' else 1

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='mode',required=True)
    for mode in ('run','child'):
        p = sub.add_parser(mode)
        p.add_argument('package',choices=LIMITS)
        if mode=='run':
            p.add_argument('label')
            p.add_argument('--seconds',type=int)
            p.add_argument('--cwd')
        p.add_argument('--network',action='store_true')
        p.add_argument('command',nargs=argparse.REMAINDER)
    p = sub.add_parser('fetch')
    p.add_argument('package',choices=LIMITS)
    p.add_argument('url');p.add_argument('output')
    p.add_argument('--maximum',type=int,required=True)
    p.add_argument('--size',type=int);p.add_argument('--expected')
    p.add_argument('--algorithm',default='sha256')
    args = parser.parse_args()
    for package in LIMITS:
        (ROOT/package/'tmp').mkdir(parents=True,exist_ok=True)
    if args.mode=='child':
        cpus = LIMITS[args.package][0]
        os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:cpus])
        restrict(ROOT/args.package,args.network)
        command = args.command[1:] if args.command[:1]==['--'] else args.command
        os.execvpe(command[0],command,os.environ)
    with (ROOT/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        return run(args) if args.mode=='run' else fetch(args)

if __name__=='__main__':
    sys.exit(main())
