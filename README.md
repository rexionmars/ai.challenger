<div align="center">
  <h1>VOLTS ENGINE INFERENCE ⚡️</h1>
  Este projeto permite a integração de varias engines voltadas para competições de xadrez, contem suporte a interface grafica, estatisticas de jogo, com suporte para CPU e GPU (nvidia series 30), com o protoloco UCI.<br>
  <p><strong>{joao_leonardi.melo, enzo.goncalves, joao_vinicius.carvalho}@somosicev.com</strong></p>
  https://discord.gg/zcZQvRvyyz
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
- [X] Windows (WSL)
- [ ] MacOS

## Features Hardware (beta) 🛠
- [x] Aceleração via CPU (intel)
- [x] Aceleração via GPU (nvidia)
- [ ] AMD graphics OpenCL.

## Estrutura de pastas do projeto 📂
```lua
ai.challenger (VOLTS ⚡️)
    |
    +--- engines/
    |       |
    |       +--- weights/
    |
    +--- performance/inference/
    |                   |            
    |                   +--- utils/Utils.py
    |                   +--- board.svg
    |                   +--- main.py 
    |
    +--- pyproject.toml
    +--- README.md
    +--- requeriments.txt
    +--- ubuntu_deps.txt
```
## Avaliação em tempo real da partida

<div align="center">
  <h4>Profundidate x Tempo de Analise</h4>
  <img src="images/Screenshot from 2023-11-20 10-49-08.png" alt="Snake logo">
  <h4>Avaliação ao longo do tempo</h4>
  <img src="images/Screenshot from 2023-11-20 14-46-31.png" alt="Snake logo">
</div>

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
