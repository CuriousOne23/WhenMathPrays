{
  "agent": "fox",
  "action": "jumps",
  "patient": "dog",
  "modifiers": ["quick","brown","lazy"]
}

const PRIMITIVES: PrimitiveFn[] = [
  InB, IIInB, IE,
  CEx, CE, ISc, TPU,
  SOB, SROB, CnOB, SmOB, SSG,
  RBU, RB, RTU, CTP,
  IdOB, TR, OuBA
]

function runPathA(raw: string): { tp: TP, trace: PrimitiveTrace[] } {
  let tp: TP = initTP(raw)
  const trace: PrimitiveTrace[] = []

  for (const fn of PRIMITIVES) {
    const inputSnapshot = structuredClone(tp)
    tp = fn(tp)
    trace.push({
      primitive: fn.name,
      input: inputSnapshot,
      output: structuredClone(tp),
      notes: primitiveNotes(fn.name, tp)
    })
  }

  return { tp, trace }
}

type PrimitiveTrace = {
  primitive: string
  input: TP
  output: TP
  notes?: string
}
