// UCIManager.cpp
/*
 * Copyright (C) 2023 João Leonardi (joao_leonardi.melo@somosicev.com)
 * Copyright (C) 2023 Enzo Morais (enzo.goncalves@somosicev.com)
 * Copyright (C) 2023 João Vinícius (joao_vinicius.carvalho@somosicev.com)
 */

// main.cpp
#include <SFML/Graphics.hpp>
#include <iostream>
#include <fstream>
#include <mutex>
#include <thread>
#include <chrono>

#include "UCIManager.h"

class ChessApp {
public:
    ChessApp() : window(sf::VideoMode(800, 600), "Chess Program"), uciManager() {
        font.loadFromFile("/path/to/your/font.ttf");
        logText.setFont(font);
        logText.setCharacterSize(14);
        logText.setPosition(500, 10);
        logText.setFillColor(sf::Color::White);
    }

    void run() {
        while (window.isOpen()) {
            handleEvents();
            update();
            render();
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }

private:
    sf::RenderWindow window;
    sf::Font font;
    sf::Text logText;
    UCIManager uciManager;

    void handleEvents() {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
        }
    }

    void update() {
        // Lógica do jogo aqui
        // ...
        updateLogWindow();
    }

    void render() {
        window.clear();
        drawChessboard();
        window.draw(logText);
        window.display();
    }

    void drawChessboard() {
        // Desenhe o tabuleiro de xadrez aqui
        // ...
    }

    void updateLogWindow() {
        std::lock_guard<std::mutex> lock(uciManager.getMutex());
        logText.setString(uciManager.getResponse());
    }
};

int main() {
    ChessApp app;
    app.run();

    return EXIT_SUCCESS;
}
