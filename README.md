# wroclaw-crispy-places
Website with interesting places of Wrocław city in Poland

## How to run
To run the program, you need:
- Python 3+
- Pip

if you want to run it in container:
- Podman (Docker can be used, but not supported yet)

With those, you can run those commands on your machine to download and run:
```bash
git clone https://github.com/trzmjel/wroclaw-crispy-places.git
cd wroclaw-crispy-places
pip install -r requirements.txt
python app.py
```
or you can simply build and run a container:
```bash
git clone https://github.com/trzmjel/wroclaw-crispy-places.git
cd wroclaw-crispy-places
podman build -t trzmjel/wroclaw-crispy-places .
podman run -d localhost/trzmjel/wroclaw-crispy-places:latest
```
