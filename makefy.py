import os
import sys
import yaml
import subprocess

# Check if PyYAML is installed, if not install it
try:
    import yaml
except ImportError:
    print("PyYAML is not installed. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
    import yaml

def validate_docker_compose(compose_file):
    """Validate the docker-compose.yml file using PyYAML."""
    try:
        with open(compose_file, 'r') as file:
            docker_compose_content = yaml.safe_load(file)
        
        # Check if it's a valid docker-compose structure
        if 'services' not in docker_compose_content:
            print("Error: The file does not contain any services definition.")
            return False, None
        return True, docker_compose_content['services']
    except yaml.YAMLError as exc:
        print(f"Error: The file is not a valid YAML file.\nDetails: {exc}")
        return False, None
    except Exception as e:
        print(f"Error: Could not open or parse the file.\nDetails: {e}")
        return False, None

def generate_makefile(compose_file, services):
    """Generate a Makefile with helpful commands."""
    
    service_targets = "\n".join([f"""
# Targets for {service}
{service}-build:
\tdocker compose -f $(COMPOSE_FILE) build {service}

{service}-rebuild:
\tdocker compose -f $(COMPOSE_FILE) build --no-cache {service}

{service}-up:
\tdocker compose -f $(COMPOSE_FILE) up -d {service}

{service}-down:
\tdocker compose -f $(COMPOSE_FILE) down {service}

{service}-prune:
\tdocker compose -f $(COMPOSE_FILE) rm -f -s -v {service}
\tdocker image prune -f

{service}-clean:
\tdocker compose -f $(COMPOSE_FILE) down --volumes {service}
\tdocker volume prune -f
\tdocker system prune -f
""" for service in services])

    makefile_content = f"""
# Makefile for Docker Compose management
COMPOSE_FILE={compose_file}

.PHONY: help build-all rebuild-all down-all prune-all clean-all { ' '.join([f'{s}-build {s}-rebuild {s}-up {s}-down {s}-prune {s}-clean' for s in services]) }

# Display help commands
help:
\t@echo "Available commands:"
\t@echo "  build-all        : Build all services using cache"
\t@echo "  rebuild-all      : Rebuild all services without cache"
\t@echo "  down-all         : Stop and remove all containers"
\t@echo "  prune-all        : Remove all containers, networks, and images"
\t@echo "  clean-all        : Remove all volumes and data"
\t@echo "  help             : Show this help message"
\t@echo "  Individual service targets:"

# Build all services with cache
build-all:
\tdocker compose -f $(COMPOSE_FILE) build

# Rebuild all services without cache
rebuild-all:
\tdocker compose -f $(COMPOSE_FILE) build --no-cache

# Bring down all containers and remove them
down-all:
\tdocker compose -f $(COMPOSE_FILE) down

# Remove all containers, networks, and images
prune-all:
\tdocker compose -f $(COMPOSE_FILE) down --volumes --rmi all

# Clean up all volumes and containers
clean-all:
\tdocker compose -f $(COMPOSE_FILE) down --volumes
\tdocker volume prune -f
\tdocker system prune -f

{service_targets}
"""

    with open('Makefile', 'w') as makefile:
        makefile.write(makefile_content)
    print("Makefile generated successfully.")

def prompt_overwrite():
    """Prompt the user to confirm overwriting the Makefile."""
    while True:
        response = input("Makefile already exists. Do you want to overwrite it? (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Invalid response. Please enter 'y' or 'n'.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python makefy.py <docker-compose.yml> [--force]")
        sys.exit(1)
    
    compose_file = sys.argv[1]
    force_overwrite = "--force" in sys.argv

    if not os.path.isfile(compose_file):
        print(f"Error: File {compose_file} does not exist.")
        sys.exit(1)
    
    # Check if Makefile exists
    if os.path.isfile('Makefile') and not force_overwrite:
        if not prompt_overwrite():
            print("Operation aborted. Makefile was not overwritten.")
            sys.exit(0)

    # Validate docker-compose.yml
    is_valid, services = validate_docker_compose(compose_file)
    
    if is_valid and services:
        generate_makefile(compose_file, services)
    else:
        print("Error: Failed to generate Makefile due to invalid docker-compose.yml.")

if __name__ == "__main__":
    main()
