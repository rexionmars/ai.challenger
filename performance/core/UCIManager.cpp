// UCIManager.cpp
/*
 * Copyright (C) 2023 João Leonardi (joao_leonardi.melo@somosicev.com)
 * Copyright (C) 2023 Enzo Morais (enzo.goncalves@somosicev.com)
 * Copyright (C) 2023 João Vinícius (joao_vinicius.carvalho@somosicev.com)
 */

#include "UCIManager.h"
#include <iostream>
#include <sstream>
#include <cstdlib>

UCIManager::UCIManager() {
    startEngine();
}

UCIManager::~UCIManager() {
    stopEngine();
}

void UCIManager::startEngine() {
    // Inicialize o Stockfish como um processo e configure a comunicação UCI
    // Caminho para o executável do Stockfish (Linux)
    std::system("../../algoritimos/stockfish/src/./stockfish");
}

void UCIManager::stopEngine() {
    // Envie o comando "quit" para encerrar o Stockfish
    sendCommand("quit");
}

void UCIManager::sendCommand(const std::string& command) {
    // Envia um comando UCI para o Stockfish
}

std::string UCIManager::getBestMove() {
    // Envie o comando "go" para obter o melhor movimento
    sendCommand("go");
    return "best_move";
}
