# golang-callgraph-with-syscalls

Callgraph generation for golang project: Usage Guide

1) Installation of golang in the os:
	Follow the link to install: https://go.dev/doc/install

2) Set env variable to use go modules:
	- export GO111MODULE=on

3) Callgraph tool usage:

	a) Clone the repository of the related package:
	- Eg: Traefik : mkdir ~/go/src/ && cd ~/go/src/ && git clone https://github.com/traefik/traefik.git

	b) Get all dependencies:
	- Eg: cd ~/go/src/traefik && go mod tidy

        c) Build callgraph tool (Optional: already exists for linux_x86_64):
	- go build callgraph.go

	d) Execute findEntrypoints script:
	- Eg: ./findEntryPoints.sh ~/go/src/traefik/

	e) Extract syscalls from generated callgraph
	- Eg: python extractsyscall.py go.src.traefik./ > traefik.syscalls
