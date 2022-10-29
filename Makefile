setupenv:
	python -m virtualenv venv
	sudo pacman -Su gobject-introspection flatpak-builder --needed
	source venv/bin/activate
	pip install - r requirements.txt
	flatpak install flathub org.gnome.Sdk/x86_64/42


test:
	pytest tests --cov=src/

lint:
	black src/
	black tests/
	flake8 src
	flake8 tests
	codespell -S venv,po

install:
	flatpak install flathub org.gnome.Sdk/x86_64/42
	flatpak install flathub org.gnome.Platform/x86_64/42
	flatpak-builder --repo=gabtag-repo python3-gabtag com.github.lachhebo.Gabtag.Devel.json --force-clean
	flatpak --user remote-add --no-gpg-verify --if-not-exists gabtag-repo gabtag-repo
	flatpak --user install gabtag-repo com.github.lachhebo.Gabtag.Devel --reinstall -y

run:
	flatpak run com.github.lachhebo.Gabtag.Devel
