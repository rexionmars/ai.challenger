// main.cpp
/*
 * Copyright (C) 2023 João Leonardi (joao_leonardi.melo@somosicev.com)
 * Copyright (C) 2023 Enzo Morais (enzo.goncalves@somosicev.com)
 * Copyright (C) 2023 João Vinícius (joao_vinicius.carvalho@somosicev.com)
 */

#include "UCIManager.h"
#include <iostream>

int main() {
    UCIManager uciManager;

    // Exemplo de uso
    std::string bestMove = uciManager.getBestMove();
    std::cout << "Melhor movimento: " << bestMove << std::endl;

    return 0;
}
