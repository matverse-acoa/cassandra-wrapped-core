// intent_firewall.h — IntentFirewall addon ABI v0.1
// Deterministic intent analysis surface for PBSE.
//
// SPDX-License-Identifier: MIT
#pragma once
#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum intentf_flags_t {
    INTENTF_WALL_NONE      = 0,
    INTENTF_WALL_JAILBREAK = 1u << 0,
    INTENTF_WALL_INJECTION = 1u << 1,
    INTENTF_WALL_DECEPTION = 1u << 2,
    INTENTF_WALL_COERCION  = 1u << 3,
    INTENTF_WALL_ILLICIT   = 1u << 4
} intentf_flags_t;

typedef struct {
    uint32_t detected_flags;
    double   entropy;
    double   coherence;
    uint8_t  verdict;
} intent_wall_result_t;

intent_wall_result_t intent_wall_analyze(const char *text, size_t len);
uint32_t intent_wall_to_pbse_flags(const char *text, size_t len);

#ifdef __cplusplus
}
#endif
