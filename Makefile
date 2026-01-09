CC ?= cc
CFLAGS ?= -O2 -std=c99 -Iinclude -Wall -Wextra -Wpedantic
LDFLAGS ?= -lm

all: intent_firewall_test

intent_firewall_test: src/intent_firewall.c tests/test_intent_firewall.c include/intent_firewall.h
	$(CC) $(CFLAGS) src/intent_firewall.c tests/test_intent_firewall.c -o $@ $(LDFLAGS)

clean:
	rm -f intent_firewall_test
