.PHONY: run

# Compute values using Make’s own variables and fallbacks
ENV_VAL := $(if $(ENVIRONMENT),$(ENVIRONMENT),$(if $(ENV),$(ENV),$(shell grep ^ENVIRONMENT .env | cut -d= -f2)))
BRW_VAL := $(if $(BROWSER),$(BROWSER),$(shell grep ^BROWSER .env | cut -d= -f2))
TAG_VAL := $(if $(TAGS),$(TAGS),@smoke)
export ENVIRONMENT := $(ENV_VAL)
export BROWSER     := $(BRW_VAL)

run:
	@echo "From Makefile: Running environment: $(ENV_VAL)"
	@echo "From Makefile: Browser set to: $(BRW_VAL)"
	@# Pass ENVIRONMENT to behave via the environment
	@ENVIRONMENT=$(ENV_VAL) BROWSER=$(BRW_VAL) behave -t $(TAG_VAL) -f allure -o allure-results

# Generate and serve Allure report
results:
	@# If a server is already running, stop it first
	@if [ -f .allure_server.pid ]; then \
		PID=$$(cat .allure_server.pid); \
		kill $$PID 2>/dev/null || true; \
		rm -f .allure_server.pid; \
		echo "Stopped existing HTTP server (PID $$PID)"; \
	fi
	@# Ensure there are results to render
	@test -d allure-results || { echo "No allure-results/ found. Run your tests first."; exit 1; }
	@# Generate a fresh report (cleans tests/reports/)
	@allure generate allure-results --clean -o tests/reports
	@echo "Serving Allure report at http://localhost:5555/"
	@PY=$$(command -v python3 >/dev/null 2>&1 && echo python3 || echo python); \
	$$PY -m http.server 5555 --directory tests/reports >/dev/null 2>&1 & echo $$! > .allure_server.pid; \
	if command -v open >/dev/null 2>&1; then open http://localhost:5555/; \
	elif command -v xdg-open >/dev/null 2>&1; then xdg-open http://localhost:5555/; fi; \
	echo "Allure report is being served (PID $$(cat .allure_server.pid))."

# Stop the local Python server AND purge previous results/reports
results-stop:
	@if [ -f .allure_server.pid ]; then \
		PID=$$(cat .allure_server.pid); \
		kill $$PID 2>/dev/null || true; \
		rm -f .allure_server.pid; \
		echo "Stopped local HTTP server (PID $$PID)"; \
	else \
		echo "No server PID file found (.allure_server.pid). Nothing to stop."; \
	fi
	@rm -rf tests/reports allure-results
	@echo "Deleted Allure outputs: tests/reports/ and allure-results/"
