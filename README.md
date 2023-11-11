# Versões Experimentais

Algoritimo: `Stockfish 16 Strong open source chess engine`<br><br>
Instalação Plataforma Linux x86_64 amd64:
Meu setup:<br>
CPU: Intel i5 12th<br>
GPU: NVIDIA RTX 3050 *Otimizada para redes neurais*<br>
Mem: 24Gb<br>

Setup para treinamento do modelo:<br>
GPU: NVIDIA Tesla T4 Neural Optimization<br>
```sh
git clone https://github.com/official-stockfish/Stockfish.git
cd Stockfish
make -j12 profile-build ARCH=x86-64-avx2
```

# Autores

- **Enzo Morais Gonçalves, João Leonardi da Silva Melo, João Vinícius Castelo branco**
  - Departamento de Engenharia de Software
  - iCev Instituto de Ensino Superior
  - Email: enzo.goncalves@somosicev.com, joao_leonardi.melo@somosicev.com, joao_vinicius.carvalho@somosicev.com

![GitHub Contributors Image](https://contrib.rocks/image?repo=rexionmars/ai.challenger)
