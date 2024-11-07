# include .env
dummy		    := $(shell touch .env)
include .env
export PYTHONPATH:=$(PWD)
export $(shell sed 's/=.*//' .env)

install: 
	curl -LsSf https://astral.sh/uv/install.sh | sh
	# source $(HOME)/.cargo/env
	uv run pip install .
	sudo apt update && sudo apt install tmux -y

run-streamlit:
	tmux new-session uv run streamlit run front/main.py --server.baseUrlPath=/absproxy/8501/

run-fastapi:
	tmux new-session uv run uvicorn api.app:app --port 5000 --reload

run: run-fastapi run-streamlit
