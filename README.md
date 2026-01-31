# cassandra-wrapped-core — PBSE Kernel

Este repositório implementa o **kernel normativo** do MatVerse.

O PBSE (Policy-Based Sovereign Execution) é um motor de decisão
**determinístico, mínimo e impessoal**.

Ele decide apenas:

PASS | BLOCK | SILENCE | ESCALATE

Com base em métricas fornecidas externamente.

---

## O que este repositório faz

- Aplica regras normativas fixas
- Gera registros canônicos encadeados por hash
- Produz decisões sem override humano
- Opera como kernel compilável (C / WASM / Python reference)

---

## O que este repositório NÃO faz

- Não mede Ψ, Ω ou CVaR
- Não executa ações
- Não mantém estado de mundo
- Não acessa rede
- Não interpreta intenção

---

## Regime Arquitetural

**REGIME: KERNEL**

Este código é deliberadamente:
- pequeno
- previsível
- restritivo

Complexidade aqui é defeito.

---

## Propriedades

- Fail-closed por construção
- Ledger encadeado (SHA3-256)
- Vetores de teste determinísticos
- ABI estável

---

## Regra Fundamental

O kernel **julga**.
Ele não explica, não executa e não corrige.
