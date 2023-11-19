<div align="center">
  <h1>VOLTS ENGINE INFERENCE ⚡️</h1>
  Este projeto permite a integração de varias engines voltadas para competições de xadrez, contem suporte a interface grafica, estatisticas de jogo, com suporte para CPU e GPU (nvidia series 30), com o protoloco UCI.<br>
  <p>{joao_leonardi.melo, enzo.goncalves, joao_vinicius.carvalho}@somosicev.com</p>
  <img src="images/Screenshot from 2023-11-18 23-50-22.png" alt="Snake logo">
</div>

## Suporte e hardware utilizado 💻
Este projeto está sendo desenvolvido inicialmente para a plataforma x86-64 amd64 Linux, ainda não tem previsão para o port de outras plataformas.<br>
Hardware principal usado no desenvolvimento atual:<br>
```sh
OS: Linux x86-64 amd4 Kernel 6.2 Genric
CPU: 12th Gen Intel® Core™ i5-12450H × 12
GPU: NVIDIA RTX 3050 Mobile Cuda cores: 2048 Neural Optimization
Mem: 24.0 GiB
TGP: 95W
```
## Plataformas Suportadas 💻
- [X] Linux
- [x] NVIDIA Jetson
- [ ] Windows
- [ ] MacOS
## Algoritimos suportados 🧬
- [ ] Leela Chess Zero (testes inicias)
- [x] Stockfish
- [ ] Alpha Zero
- [ ] Minmax (integração manual)

## Features Hardware (beta) 🛠
- [x] Aceleração via CPU (intel)
- [x] Aceleração via GPU (nvidia)
- [ ] AMD graphics OpenCL.

## Estrutura de pastas do projeto 📂
```lua
ai.challenger (VOLTS ⚡️)
    |
    +--- engine/ -- Engines
    |     |
    |     +--- Lc0
    |     +--- stockfish
    |
    +-- performance/inference -- Inferência para a comunicação com as engines.
    |             |
    |             +--- main.cpp
    |             +--- UCIManager.cpp
    |             +--- UCIManager.h
    |             +--- chess_program -- binario na arquitetura x86-64 Linux contem a inferencia ao protocolo UCI.
    |
    +-- UI
        |
        +--- config/
        +--- utils/
        +--- venv/
        +--- main.py
```

## Instalção dos algoritmos
*OBS: make -j12 somente para processadores com 12 nucleos, se o seu tiver menos ou mais nucleos, use conforme o necessario*<br>
**Instalação do Stockfish 🐟**
```sh
git clone https://github.com/official-stockfish/Stockfish.git
cd Stockfish
make -j12 profile-build ARCH=x86-64-avx2
```

**Instalação do Leela Chess Zero Linux ubuntu 😈**

Documentação complete: https://github.com/LeelaChessZero/lc0

Instalar o backend:
   - Se você deseja usar placas de vídeo NVidia, instale o CUDA e cuDNN.
   - Se você deseja usar placas de vídeo AMD, instale o OpenCL.

Entre no diretorio lc0/<br>
Execute ./build.sh<br>
O binariyo `lc0` (x84_64 Linux) estará no diretório lc0/build/release/<br>
Descompacte uma rede neural no mesmo diretório do binário. https://lczero.org/play/networks/bestnets/

Se desejar compilar com um compilador diferente, passe as variáveis de ambiente CC e CXX:
```sh
CC=clang-6.0 CXX=clang++-6.0 ./build.sh
```

## Projetos e papers usados como inspiração 📄
**Papers:**<br>
Chess AI: Competing Paradigms for Machine Intelligence:
https://arxiv.org/pdf/2109.11602.pdf<br>
Neural Networks for Chess
https://arxiv.org/pdf/2209.01506.pdf

**Bibliotecas**<br>
*Autor: João Leonardi*<br>
<br>**Neural Network Library for C lang 🧠**<br>
A collection of library for Deep Learning
https://github.com/rexionmars/neural-network-library
<br>**CTorch 🔥**<br>
A next library stb-style header-only library for Neural Networks
https://github.com/rexionmars/ctorch

# Autores
```lua
--- Departamento de Engenharia de Software
--- iCev Instituto de Ensino Superior

João Leonardi da Silva Melo
João Vinícius Castelo branco
Enzo Morais Gonçalves
Email:
  joao_leonardi.melo@somosicev.com
  joao_vinicius.carvalho@somosicev.com
  enzo.goncalves@somosicev.com
```

![GitHub Contributors Image](https://contrib.rocks/image?repo=rexionmars/ai.challenger)
