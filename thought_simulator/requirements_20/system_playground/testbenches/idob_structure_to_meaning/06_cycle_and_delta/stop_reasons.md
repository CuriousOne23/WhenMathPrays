# Stop reasons

| resolution_status | Meaning of the freeze |
|-------------------|------------------------|
| stable | Meaning delta fell below epsilon_meaning |
| identity_stable | Identity delta fell below epsilon_identity first |
| budget_exhausted | idob_search_budget_used >= max |
| time_exhausted | Supervisor / bench forced stop |

Instrument rule: the string in the packet is the halt.
If they disagree, the measurement is architectural error (improper).
