# TS Kernel (first landing)

The kernel orchestrates. It does not process.

It owns:

- TP residency for one pipeline run
- tick
- schedule from `pipelines/<stage>/pipeline.yaml`
- legality of names via the registry
- replay freeze of the returned TP

It does not own meaning, ΔH, next_context, or primitive write-sets.

## Registry

The registry is the only new object.

- Key = folder name = yaml name = `PRIMITIVE_NAME`
- No aliases, no case games
- Callable = module-level `process(tp, mode="general", **kwargs)`
- Load only names listed in the current pipeline yaml
- Unknown / stub / name mismatch = legality failure

Import root:

```
thought_simulator.requirements_20.system_playground.primitives.<name>.<name>
```

## Files (this cut)

- `registry.py` — `load(name)`
- `kernel.py` — ordered `process` calls + tick
- `pipeline_runner.py` — load yaml + fixture, hand to kernel
- `legality.py` — every yaml name must load
- `replay.py` — `freeze(tp)`; two runs compared by the runner

Not in this cut: scheduler beyond yaml order, TP manager, freeze/commit protocol,
modes (isolation / exploration / debug).

## Call loop

```
tp = fixture
for name in spec:
    tp = registry.load(name).process(tp, mode="general")
return tp
```
