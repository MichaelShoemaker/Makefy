# Makefy

**Makefy** is a Python tool that validates Docker Compose files and generates a `Makefile` with useful Docker Compose commands, allowing you to easily manage services like building, rebuilding, cleaning, and more. It also features a prompt to avoid overwriting an existing `Makefile` and provides a `--force` option for skipping this prompt.

## Features

- **Validates Docker Compose files**: Ensures the provided `docker-compose.yml` file is valid.
- **Generates a `Makefile`**: Automatically generates a `Makefile` with commands for building, rebuilding, cleaning, and managing individual services.
- **Service-specific commands**: Each Docker Compose service gets its own set of targets (e.g., `flask_app-build`, `redis-clean`).
- **Overwrite protection**: Checks for an existing `Makefile` and prompts the user before overwriting it, unless the `--force` option is used.

## Requirements

- Python 3.x
- PyYAML library (automatically installed if missing)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MichaelShoemaker/makefy.git
    ```

2. Navigate to the directory:
    ```bash
    cd makefy
    ```

3. Install dependencies (if necessary):
    ```bash
    pip install pyyaml
    ```

## Usage

1. To generate a `Makefile` from a `docker-compose.yml` file, run:
    ```bash
    python makefy.py <docker-compose.yml>
    ```

   If a `Makefile` already exists, the program will prompt you before overwriting it:
    ```
    Makefile already exists. Do you want to overwrite it? (y/n):
    ```

2. To force the creation of a `Makefile` without the prompt, use the `--force` option:
    ```bash
    python makefy.py <docker-compose.yml> --force
    ```

## Commands in the Generated `Makefile`

The `Makefile` includes commands for all services defined in your `docker-compose.yml`. Here are the key commands:

### Global Commands
- **`build-all`**: Build all services using Docker cache.
- **`rebuild-all`**: Rebuild all services without using cache.
- **`down-all`**: Stop and remove all containers.
- **`prune-all`**: Remove all containers, networks, and images.
- **`clean-all`**: Remove all volumes and clean up unused resources.

### Per-Service Commands
For each service (e.g., `flask_app`, `redis`), Makefy generates specific commands:
- **`<service>-build`**: Build the service using Docker cache.
- **`<service>-rebuild`**: Rebuild the service without Docker cache.
- **`<service>-up`**: Start the service.
- **`<service>-down`**: Stop and remove the service.
- **`<service>-prune`**: Remove the service and associated resources.
- **`<service>-clean`**: Clean up volumes and unused resources for the service.

## Example

Given a `docker-compose.yml` with services `flask_app` and `redis`, you can:

- Build `flask_app` without cache:
    ```bash
    make flask_app-rebuild
    ```

- Clean up all volumes for `redis`:
    ```bash
    make redis-clean
    ```

- Build all services using cache:
    ```bash
    make build-all
    ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss changes or improvements.

## License

This project is licensed under the MIT License.
