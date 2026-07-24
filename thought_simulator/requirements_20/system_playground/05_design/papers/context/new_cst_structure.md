Absolutely, Jeff — and you framed the architectural motivation perfectly. Splitting CST into **three atomized units** (CST‑Core, CST‑MS, CST‑Mux) gives you cleaner simulation, cleaner documentation, cleaner code, and cleaner testbenches.

Since you asked for **new_cst_structure.md**, I’ll draft the full document for you — structured, precise, and ready to drop into your repo.

---

# **new_cst_structure.md**

## **Overview**
The Context Stability Tracker (CST) was originally implemented as a single monolithic module responsible for all stability detection, merge/split detection, structural compensation, and signal packaging. As Path‑A evolved, this design became increasingly difficult to maintain, simulate, and document.

To address these issues, CST has been decomposed into **three independent, atomized units**:

1. **CST‑Core** — instantaneous stability detection  
2. **CST‑MS** — merge/split structural detection  
3. **CST‑Mux** — unified signal aggregator for CIL  

This new structure preserves the independence of each functional domain while keeping the CIL interface simple and stable.

---

## **Why CST Was Split**
The original CST module had several architectural problems:

### **1. Mixed responsibilities**
CST was simultaneously responsible for:
- instantaneous stability detection  
- long‑horizon merge/split detection  
- structural compensation  
- signal packaging  
- lineage interpretation  

These responsibilities have different time horizons, different algorithms, and different state requirements. Combining them created unnecessary coupling.

### **2. Difficult simulation**
System simulation needed to:
- isolate merge/split behavior  
- isolate drift/oscillation/collapse behavior  
- test each independently  
- evolve each independently  

A monolithic CST made this impossible without complex scaffolding.

### **3. Documentation bloat**
The CST requirements file mixed:
- stability rules  
- merge/split rules  
- lineage rules  
- packaging rules  

This made the document long, hard to read, and hard to version.

### **4. Testbench entanglement**
The CST testbench had to simulate:
- drift  
- oscillation  
- collapse  
- ambiguity  
- merge  
- split  
- lineage continuity  
- signal packaging  

This made the testbench large, brittle, and difficult to extend.

### **5. CIL interface complexity**
CIL had to accept multiple CST signal streams:
- stability signals  
- merge/split signals  
- structural compensation signals  

This forced CIL to understand CST internals, violating modularity.

---

## **The New CST Structure**

### **1. CST‑Core**  
**Responsibility:** instantaneous stability detection  
**Time horizon:** per‑turn, stateless  
**Signals produced:**  
- drift  
- oscillation  
- collapse  
- freeze/thaw  
- ambiguity  
- lineage stability  

**Key properties:**  
- simple  
- deterministic  
- independent  
- easy to simulate  
- easy to document  
- easy to test  

CST‑Core handles all “normal” stability signals that do not require long‑horizon analysis.

---

### **2. CST‑MS (Merge/Split Detector)**  
**Responsibility:** long‑horizon structural detection  
**Time horizon:** multi‑turn, stateful  
**Signals produced:**  
- merge  
- split  

**Key properties:**  
- convergence/divergence detection  
- 10‑turn buffers  
- monotonic thresholds  
- replay determinism  
- independent state machine  

CST‑MS is responsible for detecting structural transitions in identity‑layer topology. It is fully independent of CST‑Core.

---

### **3. CST‑Mux (Signal Aggregator)**  
**Responsibility:** unify CST‑Core and CST‑MS outputs  
**Time horizon:** per‑turn  
**Signals produced:**  
- unified CSTSignals object for CIL  

**Key properties:**  
- merges two independent CST streams  
- keeps CIL interface simple  
- hides CST internals  
- maintains modularity  
- no detection logic  
- no thresholds  
- no state machine  

CST‑Mux is a pure multiplexer. It exists solely to keep CIL decoupled from CST’s internal architecture.

---

## **Why Three Units Is the Correct Architecture**

### **1. CST‑Core and CST‑MS are independent**
They operate on different time horizons and different algorithms. Their independence causes no interference.

### **2. CST‑Mux preserves modularity**
Without CST‑Mux, CIL would need to accept multiple CST inputs, forcing CIL to understand CST internals. CST‑Mux prevents this.

### **3. Atomized documentation**
Each unit has its own requirement file:
- CST‑Core requirements  
- CST‑MS requirements  
- CST‑Mux requirements  

This keeps documentation short, focused, and easy to maintain.

### **4. Atomized programs**
Each unit has its own Python module:
- cst_core.py  
- cst_ms.py  
- cst_mux.py  

This keeps code clean and maintainable.

### **5. Atomized testbenches**
Each unit has its own testbench:
- cst_core_testbench.py  
- cst_ms_testbench.py  
- cst_mux_testbench.py  

This keeps testing simple and isolated.

### **6. Cleaner system simulation**
Simulation can now:
- test stability independently  
- test merge/split independently  
- test signal packaging independently  

This dramatically simplifies system_playground and system_simulation.

---

## **Summary**
The new CST structure is:

```
CST
 ├── CST-Core   (instantaneous stability)
 ├── CST-MS     (merge/split detection)
 └── CST-Mux    (signal aggregator → CIL)
```

This architecture is:
- modular  
- maintainable  
- testable  
- simulation‑friendly  
- documentation‑friendly  
- future‑proof  

It resolves the problems of the monolithic CST and sets a clean foundation for Path‑A’s continued evolution.

---
