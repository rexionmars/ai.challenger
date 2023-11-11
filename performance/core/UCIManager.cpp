// UCIManager.cpp
/*
 * Copyright (C) 2023 João Leonardi (joao_leonardi.melo@somosicev.com)
 * Copyright (C) 2023 Enzo Morais (enzo.goncalves@somosicev.com)
 * Copyright (C) 2023 João Vinícius (joao_vinicius.carvalho@somosicev.com)
 */

#include "UCIManager.h"
#include <iostream>
#include <fstream>
#include <unistd.h>

UCIManager::UCIManager() {
    startEngine();
    sendCommand("uci");
    sendCommand("isready");
}

UCIManager::~UCIManager() {
    stopEngine();
}

void UCIManager::startEngine() {
    // Substitua "./stockfish" pelo caminho real para o executável do Stockfish
    if (std::system("/home/remix/workdir/ai.challenger/algoritimos/stockfish/src/stockfish") == -1) {
        std::cerr << "Erro ao iniciar o Stockfish." << std::endl;
        std::exit(EXIT_FAILURE);
    }
}


void UCIManager::stopEngine() {
    sendCommand("quit");
    if (stockfishProcess) {
        pclose(stockfishProcess);
    }
}

void UCIManager::sendCommand(const std::string& command) {
    if (stockfishProcess) {
        fprintf(stockfishProcess, "%s\n", command.c_str());
        fflush(stockfishProcess);
    } else {
        std::cerr << "Stockfish não inicializado corretamente." << std::endl;
        std::exit(EXIT_FAILURE);
    }
}

std::string UCIManager::getBestMove() {
    sendCommand("position startpos"); // Configura a posição inicial (pode ser ajustada conforme necessário)
    sendCommand("go movetime 1000");  // Solicita um movimento com um tempo limite de 1000 milissegundos

    // Agora, leia a resposta do Stockfish
    std::string bestMove;
    std::ifstream stockfishOutput("stockfish_output.txt"); // Arquivo temporário para armazenar a saída do Stockfish
    if (stockfishOutput.is_open()) {
        std::getline(stockfishOutput, bestMove);
        stockfishOutput.close();
    } else {
        std::cerr << "Erro ao abrir o arquivo de saída do Stockfish." << std::endl;
    }

    return bestMove;
}
