PLATFORM=$(shell uname)

ifeq ($(PLATFORM),Darwin)

renderer/application.macosx:
	@echo "Please use processing to generate the renderer (see README)"
	@exit 1

install: renderer/application.macosx
	mkdir -p /usr/bin/prender
	cp renderer/application.macosx/renderer.app/Contents/Resources/Java/*jar /usr/bin/prender
	cp renderer/renderer /usr/bin/prender

else

# Assume anything other than Darwin is Linux...

renderer/application.linux:
	@echo "Please use processing to generate the renderer (see README)"
	@exit 1

install: renderer/application.linux
	mkdir -p /usr/bin/prender
	cp renderer/application.linux/renderer /usr/bin/prender
	cp -r renderer/application.linux/lib /usr/bin/prender

endif

