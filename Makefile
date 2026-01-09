CC ?= cc
CFLAGS ?= -O2 -std=c99 -Iinclude -Wall -Wextra -Wpedantic
LDFLAGS ?= -lm

SRC_DIR := src
TEST_DIR := tests
INCLUDE_DIR := include
INTENT_FIREWALL_TEST_BIN := intent_firewall_test

.PHONY: all clean

all: $(INTENT_FIREWALL_TEST_BIN)

$(INTENT_FIREWALL_TEST_BIN): $(SRC_DIR)/intent_firewall.c $(TEST_DIR)/test_intent_firewall.c $(INCLUDE_DIR)/intent_firewall.h
	$(CC) $(CFLAGS) $(SRC_DIR)/intent_firewall.c $(TEST_DIR)/test_intent_firewall.c -o $@ $(LDFLAGS)

clean:
	rm -f $(INTENT_FIREWALL_TEST_BIN)
