# Variables
SUDO = sudo
PYTHON = python3
SCRIPT = network.py
SRC_DIR = src/
PCAP_DIR = pcap/
LOG_DIR = logs/
MININET_LOG_DIR = log/
P4I_FILES = *.p4i
JSON_FILES = *.json

# Targets
.PHONY: run clean init

# Run the P4 simulation script
run:
	@echo "Running the P4 network simulation..."
	$(SUDO) $(PYTHON) $(SRC_DIR)$(SCRIPT)

# Clean up generated files, Mininet, logs, and temporary files
clean:
	@echo "Cleaning up PCAP, logs, Mininet files, P4I, and JSON files..."
	$(SUDO) rm -rf $(SRC_DIR)$(PCAP_DIR) $(SRC_DIR)$(LOG_DIR) $(SRC_DIR)$(MININET_LOG_DIR)
	$(SUDO) rm -f $(SRC_DIR)$(P4I_FILES) $(SRC_DIR)$(JSON_FILES)
	@echo "Running Mininet cleanup..."
	$(SUDO) mn -c
	@echo "Cleanup complete!"

# Initialize necessary directories
init:
	@echo "Creating necessary directories..."
	mkdir -p $(SRC_DIR)$(PCAP_DIR) $(SRC_DIR)$(LOG_DIR) $(SRC_DIR)$(MININET_LOG_DIR)
	@echo "Directories initialized!"
