# Variables
PYTHON = python3
SCRIPT = network.py
PCAP_DIR = pcap/
LOG_DIR = logs/
MININET_LOG_DIR = log/

# Targets
.PHONY: run clean init

# Run the P4 simulation script
run:
	@echo "Running the P4 network simulation..."
	$(PYTHON) $(SCRIPT)

# Clean up generated files, Mininet, and logs
clean:
	@echo "Cleaning up PCAP, logs, and Mininet files..."
	rm -rf $(PCAP_DIR) $(LOG_DIR) $(MININET_LOG_DIR)
	@echo "Running Mininet cleanup..."
	sudo mn -c
	@echo "Cleanup complete!"

# Initialize necessary directories
init:
	@echo "Creating necessary directories..."
	mkdir -p $(PCAP_DIR) $(LOG_DIR) $(MININET_LOG_DIR)
	@echo "Directories initialized!"
