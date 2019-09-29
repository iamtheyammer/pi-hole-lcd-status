freeze:
	pip3 freeze > requirements.txt

install:
	pip3 install --no-cache-dir -r requirements.txt

run:
	source .env && python3 src/main.py

buildenv:
	touch docker_env.txt
	echo Using your current DNS resolver as the Pi-hole server address.
	echo Modify docker_env.txt to change it.
	echo PIHOLEMON_HOSTNAME=http://`cat /etc/resolv.conf |grep -i '^nameserver'|head -n1|cut -d ' ' -f2` >> docker_env.txt
	echo PIHOLEMON_DEBUG=false >> docker_env.txt

dockerbuild:
	docker build --tag piholemon .

dockerrund:
	if [ ! -f docker_env.txt ]; then echo Missing docker env file, run make buildenv first; exit; fi;
	docker run --privileged --env-file docker_env.txt -d piholemon
