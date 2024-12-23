app:
	poetry run streamlit run src/app.py

load_data:
	echo "$@"
	poetry run python src/commands/load_data.py $(file_name)
