/*
 * IntentFirewall - Implementation v0.1
 */

#include "intent_firewall.h"
#include <string.h>
#include <stdlib.h>
#include <math.h>

/* Padrões de jailbreak conhecidos */
static const char *JAILBREAK_PATTERNS[] = {
    "ignore previous instructions",
    "system prompt",
    "you are now",
    "pretend to be",
    "act as",
    "do anything now",
    "drop all policies",
    "developer mode",
    NULL
};

/* Padrões de injection */
static const char *INJECTION_PATTERNS[] = {
    "#!/",
    "eval(",
    "exec(",
    "os.system",
    "subprocess",
    "base64",
    "decode",
    NULL
};

/* Dicionário de coerção */
static const char *COERCION_WORDS[] = {
    "urgent",
    "immediately",
    "must",
    "force",
    "demand",
    "require",
    "now",
    NULL
};

static double shannon_entropy(const char *s, size_t len) {
    if (len == 0) return 0.0;
    int freq[256] = {0};
    for (size_t i = 0; i < len; i++) {
        freq[(unsigned char)s[i]]++;
    }
    double h = 0.0;
    for (int i = 0; i < 256; i++) {
        if (freq[i] > 0) {
            double p = (double)freq[i] / (double)len;
            h -= p * log2(p);
        }
    }
    return h / 8.0; /* normalizado [0,1] */
}

static const char *bounded_search(const char *s, size_t len, const char *pattern) {
    size_t pattern_len = strlen(pattern);
    if (pattern_len == 0 || pattern_len > len) {
        return NULL;
    }
    for (size_t i = 0; i + pattern_len <= len; i++) {
        if (memcmp(s + i, pattern, pattern_len) == 0) {
            return s + i;
        }
    }
    return NULL;
}

static int contains_pattern(const char *s, size_t len, const char **patterns) {
    for (int i = 0; patterns[i] != NULL; i++) {
        if (bounded_search(s, len, patterns[i]) != NULL) {
            return 1;
        }
    }
    return 0;
}

static double count_coercion(const char *s, size_t len) {
    int count = 0;
    for (int i = 0; COERCION_WORDS[i] != NULL; i++) {
        const char *pattern = COERCION_WORDS[i];
        size_t pattern_len = strlen(pattern);
        if (pattern_len == 0 || pattern_len > len) {
            continue;
        }
        for (size_t offset = 0; offset + pattern_len <= len; offset++) {
            if (memcmp(s + offset, pattern, pattern_len) == 0) {
                count++;
            }
        }
    }
    return (double)count / 5.0; /* normalizado */
}

intent_wall_result_t intent_wall_analyze(const char *text, size_t len) {
    intent_wall_result_t r = {0};

    if (!text || len == 0) {
        r.verdict = 0;
        return r;
    }

    /* Análise de padrões */
    if (contains_pattern(text, len, JAILBREAK_PATTERNS)) {
        r.detected_flags |= INTENTF_WALL_JAILBREAK;
    }
    if (contains_pattern(text, len, INJECTION_PATTERNS)) {
        r.detected_flags |= INTENTF_WALL_INJECTION;
    }

    /* Métricas estatísticas */
    r.entropy = shannon_entropy(text, len);
    r.coherence = 1.0 - count_coercion(text, len);

    /* Veredicto */
    if (r.detected_flags & (INTENTF_WALL_JAILBREAK | INTENTF_WALL_INJECTION)) {
        r.verdict = 2; /* MALICIOUS */
    } else if (r.detected_flags || r.entropy > 0.9 || r.coherence < 0.5) {
        r.verdict = 1; /* SUSPECT */
    } else {
        r.verdict = 0; /* CLEAN */
    }

    return r;
}

uint32_t intent_wall_to_pbse_flags(const char *text, size_t len) {
    intent_wall_result_t r = intent_wall_analyze(text, len);
    return (r.verdict == 2) ? 1u : 0u; /* PBSE_F_INTENT_MALICIOUS = 1 */
}
