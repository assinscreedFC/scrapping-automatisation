.PHONY: snapshot clean

snapshot:
	@echo "=== Arborescence du projet ===" > code.txt
	@tree -I '__pycache__|*.pyc|*.git' >> code.txt
	@echo "\n=== Contenu des fichiers Python ===" >> code.txt
	@find . -name "*.py" ! -path "*/__pycache__/*" | while read file; do \
		echo "\n----- $$file -----" >> code.txt; \
		cat "$$file" >> code.txt; \
	done
	@echo "\nSnapshot généré dans code.txt"

clean:
	@rm -f code.txt
	@echo "code.txt supprimé"
