# include .env

# export $(shell sed 's/=.*//' .env)

run:
	@export $(shell grep -v '^#' .env | xargs) && uv run streamlit run front/main.py --server.baseUrlPath=/absproxy/8501/