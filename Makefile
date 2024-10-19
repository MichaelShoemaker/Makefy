
# Makefile for Docker Compose management
COMPOSE_FILE=docker-compose.yml

.PHONY: help build-all rebuild-all down-all prune-all clean-all flask_app-build flask_app-rebuild flask_app-up flask_app-down flask_app-prune flask_app-clean redis-build redis-rebuild redis-up redis-down redis-prune redis-clean

# Display help commands
help:
	@echo "Available commands:"
	@echo "  build-all        : Build all services using cache"
	@echo "  rebuild-all      : Rebuild all services without cache"
	@echo "  down-all         : Stop and remove all containers"
	@echo "  prune-all        : Remove all containers, networks, and images"
	@echo "  clean-all        : Remove all volumes and data"
	@echo "  help             : Show this help message"
	@echo "  Individual service targets:"

# Build all services with cache
build-all:
	docker compose -f $(COMPOSE_FILE) build

# Rebuild all services without cache
rebuild-all:
	docker compose -f $(COMPOSE_FILE) build --no-cache

# Bring down all containers and remove them
down-all:
	docker compose -f $(COMPOSE_FILE) down

# Remove all containers, networks, and images
prune-all:
	docker compose -f $(COMPOSE_FILE) down --volumes --rmi all

# Clean up all volumes and containers
clean-all:
	docker compose -f $(COMPOSE_FILE) down --volumes
	docker volume prune -f
	docker system prune -f


# Targets for flask_app
flask_app-build:
	docker compose -f $(COMPOSE_FILE) build flask_app

flask_app-rebuild:
	docker compose -f $(COMPOSE_FILE) build --no-cache flask_app

flask_app-up:
	docker compose -f $(COMPOSE_FILE) up -d flask_app

flask_app-down:
	docker compose -f $(COMPOSE_FILE) down flask_app

flask_app-prune:
	docker compose -f $(COMPOSE_FILE) rm -f -s -v flask_app
	docker image prune -f

flask_app-clean:
	docker compose -f $(COMPOSE_FILE) down --volumes flask_app
	docker volume prune -f
	docker system prune -f


# Targets for redis
redis-build:
	docker compose -f $(COMPOSE_FILE) build redis

redis-rebuild:
	docker compose -f $(COMPOSE_FILE) build --no-cache redis

redis-up:
	docker compose -f $(COMPOSE_FILE) up -d redis

redis-down:
	docker compose -f $(COMPOSE_FILE) down redis

redis-prune:
	docker compose -f $(COMPOSE_FILE) rm -f -s -v redis
	docker image prune -f

redis-clean:
	docker compose -f $(COMPOSE_FILE) down --volumes redis
	docker volume prune -f
	docker system prune -f

