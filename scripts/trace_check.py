#!/usr/bin/env python3
import json,pathlib,re,sys
out=pathlib.Path(sys.argv[1]); errors=[]; gaps=[]
def read(p):return json.loads(pathlib.Path(p).read_text())
r=read('trace/requirements.json'); sources={s['id']:s for s in read('trace/sources.json')['sources']}
tests={t['id']:t for t in read('trace/tests.json')['tests']}
assumptions={a['id'] for a in r['assumptions']}
lean='\n'.join(p.read_text() for p in pathlib.Path('LeanCpOs').glob('*.lean'))
c='\n'.join(p.read_text() for p in pathlib.Path('build').glob('*.c'))
decls={'LeanCpOs.'+n for n in re.findall(r'^(?:def|structure|inductive|theorem) ([\w.]+)',lean,re.M)}
all_thms={'LeanCpOs.'+n for n in re.findall(r'^theorem (\w+)',lean,re.M)}
seen=set(); used=set(); reverse={}; rows=[]
audit=read(out/'axioms.json') if (out/'axioms.json').exists() else {'theorems':[]}
proved={x['theorem'] for x in audit['theorems'] if x['status']=='checked'}
testpath=out/'test-results/tests.json'
executed={t['id']:t['status'] for t in read(testpath)['tests']} if testpath.exists() else {}
if (out/'control-flow.log').exists():
    executed['T-CONTROL']='passed' if 'PASS T-CONTROL:' in (out/'control-flow.log').read_text() else 'failed'
for q in r['requirements']:
    ident=q['id']
    if ident in seen:errors.append('duplicate '+ident)
    seen.add(ident)
    for a in q['assumptions']:
        if a not in assumptions:errors.append(f'{ident}: unknown assumption {a}')
    for s in q['sources']:
        if s['document'] not in sources:errors.append(f'{ident}: unknown source')
        elif sources[s['document']]['sha256'] is None and sources[s['document']]['kind']!='project-decision':
            gaps.append(f'{ident}: source PDF hash unavailable: '+s['document'])
    for d in q['definitions']+q['theorems']:
        if d not in decls:errors.append(f'{ident}: missing declaration {d}')
    used.update(q['theorems'])
    for t in q['tests']:
        if t not in tests:errors.append(f'{ident}: missing test {t}')
    for f in q['files']+q['boundaries']:
        if not pathlib.Path(f).is_file():errors.append(f'{ident}: missing file {f}')
    for sym in q['generated_symbols']:
        if not re.search(r'\b'+re.escape(sym)+r'\s*\(',c):errors.append(f'{ident}: missing generated symbol {sym}')
    row=dict(q)
    row['proof']='checked' if q['theorems'] and all(t in proved for t in q['theorems']) else 'unproved'
    statuses=[executed.get(t,'not_run') for t in q['tests']]
    row['test']=('failed' if 'failed' in statuses else 'not_run' if not statuses or 'not_run' in statuses else 'passed')
    if q['scope']=='deferred':gaps.append(f'{ident}: deferred/unimplemented/unproved/not_run')
    elif row['proof']!='checked':gaps.append(f'{ident}: no checked proof for this boundary')
    if row['test']!='passed':gaps.append(f'{ident}: tests {row["test"]}')
    # Symmetric indices are generated from the very same edges, not hand duplicated.
    keys=q['definitions']+q['theorems']+q['generated_symbols']+q['tests']+q['files']+q['boundaries']+[s['document']+':'+s['section'] for s in q['sources']]
    for key in keys:reverse.setdefault(key,[]).append(ident)
    rows.append(row)
for t in all_thms-used:errors.append('untraced theorem '+t)
result=dict(structural_status='passed' if not errors else 'failed',coverage_status='incomplete' if gaps else 'complete',errors=errors,gaps=sorted(set(gaps)),requirements=rows,reverse={k:sorted(set(v)) for k,v in reverse.items()})
(out/'trace.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(structural_status=result['structural_status'],coverage_status=result['coverage_status'],errors=errors,gaps=result['gaps']),indent=2))
sys.exit(bool(errors))
