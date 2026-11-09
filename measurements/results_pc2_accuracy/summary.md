# PC2 RTX 5070 Ti — GQA/POPE/MME, max_new_tokens 16, FP16 (2026-10-26)

| method | setting | GQA acc | POPE F1 | MME perception_total | n (GQA/POPE/MME) |
|---|---|---|---|---|---|
| base | default | 61.97 | 85.87 | 1528.1 | 12578/9000/2374 |
| vispruner | default | 57.92 | 84.23 | 1463.3 | 12578/9000/2374 |
| vispruner | r889 | 55.52 | 80.38 | 1372.6 | 12578/9000/2374 |
| cdpruner_fix | default | 59.80 | 87.51 | 1465.5 | 12578/9000/2374 |
| cdpruner_fix | r889 | 58.73 | 87.54 | 1414.7 | 12578/9000/2374 |
| sparsevlm | default | 59.43 | 85.35 | 1459.8 | 12578/9000/2374 |
| sparsevlm | r889 | 53.63 | 77.63 | 1296.3 | 12578/9000/2374 |
| dart | default | 58.97 | 80.36 | 1482.5 | 12578/9000/2374 |
| dart | r889 | 56.37 | 74.21 | 1420.4 | 12578/9000/2374 |
