Instalção stockfish

Meu setup:
CPU: i5 12th
CPU: NVIDIA RTX 3050 4Gb

```sh
git clone https://github.com/official-stockfish/Stockfish.git
cd src
make -j12 profile-build ARCH=x86-64-avx2
```

