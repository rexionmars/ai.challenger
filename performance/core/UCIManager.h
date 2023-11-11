// UCIManager.h
/*
 * Copyright (C) 2023 João Leonardi (joao_leonardi.melo@somosicev.com)
 * Copyright (C) 2023 Enzo Morais (enzo.goncalves@somosicev.com)
 * Copyright (C) 2023 João Vinícius (joao_vinicius.carvalho@somosicev.com)
 */

#pragma once

#include <string>

class UCIManager {
public:
    UCIManager();
    ~UCIManager();

    void startEngine();
    void stopEngine();
    void sendCommand(const std::string& command);
    std::string getBestMove();
private:
    FILE* stockfishProcess;
};
