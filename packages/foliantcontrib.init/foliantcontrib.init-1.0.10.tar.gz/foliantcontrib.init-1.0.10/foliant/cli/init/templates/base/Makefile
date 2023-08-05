all:
	make pdf
	make docx
	make site
	make confluence
	make pre

pdf:
	docker-compose run --rm foliant make pdf --with pandoc

docx:
	docker-compose run --rm foliant make docx

site:
	docker-compose run --rm foliant make site

confluence:
	docker-compose run --rm foliant make confluence

pre:
	docker-compose run --rm foliant make pre
