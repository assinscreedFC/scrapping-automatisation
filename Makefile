.PHONY: snapshot clean run install

snapshot:
	@echo "=== Arborescence du projet ===" > code.txt
	@tree -I '__pycache__|*.pyc|*.git|venv|scrap/data' >> code.txt
	@echo "\n=== Contenu des fichiers Python ===" >> code.txt
	@find . -name "*.py" \
		! -path "*/__pycache__/*" \
		! -path "./venv/*" \
		! -path "./scrap/data/*" \
		! -path "./.git/*" \
	| while read file; do \
		echo "\n----- $$file -----" >> code.txt; \
		cat "$$file" >> code.txt; \
	done
	@echo "\nSnapshot généré dans code.txt"

clean:
	@rm -f code.txt
	@echo "code.txt supprimé"

run:
	@echo "Démarrage du bot..."
	@python -m bot.main

install:
	@echo "Installation des dépendances..."
	@pip install -r requirements.txt
