# Just
Just commands are defined in `justfile`. Run `just` without arguments to see all available recipes.

Common commands:
- `just` - List all recipes
- `just shell` - Django shell
- `just migrate` - Run migrations
- `just check` - Django system check
- `just up` - Start Docker containers
- `just down` - Stop and remove Docker containers
- `just ps` - Show container status
- `just restart` - Restart containers
- `just pull_new_patch` - Pull, migrate, and restart services
- `just suit-simple <model> <app>` - Generate CRUD for a simple model
- `just suit-fk <parent> <child> <app>` - Generate CRUD for a model with ForeignKey
- `just populate model <app.model> <count>` - Create test data
