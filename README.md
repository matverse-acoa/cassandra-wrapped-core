# PBSE Kernel v0.1 (REAL)

Kernel normativo determinístico: PASS/BLOCK/SILENCE/ESCALATE + SHA3-256 ledger chain.

## Compilar (native)
```bash
cc -O2 -std=c99 -Isrc -Iinclude src/tiny_sha3.c src/pbse_kernel.c src/pbse_cli.c -o pbse_cli -lm
```

## Rodar (native)
```bash
./pbse_cli --input-hash 00...00 --prev-root 11...11 --unix-ns 1700000000000000000 --run-id 1 \
  --flags 0 --phi 0.9 --omega 0.9 --theta 0.9 --phi-min 0.77 --omega-min 0.70 --theta-min 0.75
```

## Rodar (python reference)
```bash
python3 python/pbse_cli.py --input-hash 00...00 --prev-root 11...11 --unix-ns 1700000000000000000 --run-id 1 \
  --flags 0 --phi 0.9 --omega 0.9 --theta 0.9 --phi-min 0.77 --omega-min 0.70 --theta-min 0.75 --json
```

## Validar vetores ouro
```bash
python3 tests/test_vectors.py
```

Record canônico (148 bytes):
- record_hash = SHA3-256(record)
- new_root    = SHA3-256(prev_root || record_hash)

Host rules: ver `HOST_CONTRACT.md`.

