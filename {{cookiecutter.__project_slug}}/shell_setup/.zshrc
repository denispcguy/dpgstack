# Load .env file if it exists in the current directory
if [ -f "$PWD/.env" ]; then
  export $(grep -v '^#' .env | xargs)
fi
