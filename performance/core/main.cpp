/*
 * Copyright (C) 2023 João Leonardi (joao_leonardi.melo@somosicev.com)
 * Copyright (C) 2023 Enzo Morais (enzo.goncalves@somosicev.com)
 * Copyright (C) 2023 João Vinícius (joao_vinicius.carvalho@somosicev.com)
 */

#include <iostream>
#include <string>
#include <cstdio>

int main() {
    FILE *stockfish = popen("../../../algoritimos/stockfish/src/stockfish", "r+");
    if (!stockfish) {
        std::cerr << "Erro ao abrir o Stockfish." << std::endl;
        return -1;
    }

    // Enviar comando para o Stockfish
    std::string comando = "uci\n";
    fprintf(stockfish, "%s", comando.c_str());
    fflush(stockfish);

    // Ler a resposta do Stockfish
    char buffer[4096];
    std::string resposta;
    while (fgets(buffer, sizeof(buffer), stockfish) != nullptr) {
        resposta += buffer;
        if (buffer[0] == '\n') break;  // Fim da resposta UCI
    }

    // Exibir resposta
    std::cout << resposta;

    // Fechar o processo do Stockfish
    pclose(stockfish);

    return 0;
}
