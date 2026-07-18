## Running the Context Subsystem Testbenches  
The `context/` directory is a Python package (because it contains `__init__.py`).  
All testbenches can be run **directly from inside this directory** using `python -m`.

### 📌 Where to run commands
Open a terminal and `cd` into:

```
thought_simulator/20_requirements/system_playground/context/
```

All commands below assume you are inside this directory.

---

## CST Testbench

Run:

```
python -m cst.cst_testbench
```

Log output:

```
python -m cst.cst_testbench > cst.log
```

`cst.log` will appear in the **context/** directory.

---

## COB Testbenches

### Standard COB Testbench

```
python -m cob.cob_testbench
```

Log:

```
python -m cob.cob_testbench > cob.log
```

### Merge/Split Structural Testbench

```
python -m cob.cob_testbench_merge_split
```

Log:

```
python -m cob.cob_testbench_merge_split > cob_merge_split.log
```

---

## CIL Testbench

```
python -m cil.cil_testbench
```

Log:

```
python -m cil.cil_testbench > cil.log
```

---

## Unified Context Testbench

```
python -m context_testbench
```

Log:

```
python -m context_testbench > context.log
```

---

## Summary

- You **can run all testbenches from inside the `context/` directory**.  
- Use `python -m context.<subsystem>.<testbench>`.  
- Log files (`> X.log`) appear in the **current directory** (context/).  
- Imports inside testbenches must use:

```
from context.cst.cst import CST
from context.cob.cob import COB
from context.cil.cil import CIL, IdentityObject
```

Everything stays clean, consistent, and easy to run.

---
