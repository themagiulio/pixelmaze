PYXEL_APP_FILE=maze.pyxapp
PYXEL_RESOURCE_FILE=maze.pyxres
STARTUP_SCRIPT_FILE=main.py

app2exe:
	@pyxel app2exe $(PYXEL_APP_FILE)

build: package app2exe

edit:
	@pyxel package $(PYXEL_RESOURCE_FILE)

package:
	@pyxel package . $(STARTUP_SCRIPT_FILE)

run:
	@pyxel run $(STARTUP_SCRIPT_FILE)

watch:
	@pyxel watch . $(STARTUP_SCRIPT_FILE)
