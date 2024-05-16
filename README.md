# wroclaw-crispy-places
Website with interesting places of Wrocław city in Poland

## How to run
To run the server, you need to have Docker/Podman with support for compose. Run those commands for:
### Podman
```bash
git clone https://github.com/trzmjel/wroclaw-crispy-places.git
cd wroclaw-crispy-places
podman build -t trzmjel/wroclaw-crispy-places .
podman compose up -d
```
### Docker
```bash
git clone https://github.com/trzmjel/wroclaw-crispy-places.git
cd wroclaw-crispy-places
docker build -t trzmjel/wroclaw-crispy-places .
docker compose up -d
```
or use podman-desktop or docker-desktop for GUI.
