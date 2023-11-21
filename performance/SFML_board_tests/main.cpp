#include <SFML/Graphics.hpp>
#include <vector>

// Função para calcular um ponto na curva de Bezier cúbica
sf::Vector2f calculateBezierPoint(float t, const sf::Vector2f& p0, const sf::Vector2f& p1, const sf::Vector2f& p2, const sf::Vector2f& p3) {
    float u = 1.0f - t;
    float tt = t * t;
    float uu = u * u;
    float uuu = uu * u;
    float ttt = tt * t;

    sf::Vector2f p = uuu * p0; // (1-t)^3 * P0
    p += 3.0f * uu * t * p1;   // 3 * (1-t)^2 * t * P1
    p += 3.0f * u * tt * p2;   // 3 * (1-t) * t^2 * P2
    p += ttt * p3;             // t^3 * P3

    return p;
}

int main() {
    // Cria uma instância de sf::RenderWindow
    sf::RenderWindow window(sf::VideoMode(800, 600), "Exemplo de Gráfico Smooth");

    // Define as coordenadas dos pontos de controle da curva de Bezier
    sf::Vector2f p0(100, 300);
    sf::Vector2f p1(200, 100);
    sf::Vector2f p2(400, 500);
    sf::Vector2f p3(600, 300);

    // Configuração dos parâmetros da curva
    const int numPoints = 100;
    std::vector<sf::Vector2f> curvePoints;

    // Gera pontos na curva de Bezier
    for (int i = 0; i <= numPoints; ++i) {
        float t = static_cast<float>(i) / static_cast<float>(numPoints);
        sf::Vector2f point = calculateBezierPoint(t, p0, p1, p2, p3);
        curvePoints.push_back(point);
    }

    // Loop principal
    while (window.isOpen()) {
        // Processa eventos
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
        }

        // Atualizações

        // Desenha a curva
        window.clear();
        for (const auto& point : curvePoints) {
            sf::CircleShape circle(2.0f); // Cria um pequeno círculo para representar cada ponto na curva
            circle.setPosition(point);
            circle.setFillColor(sf::Color::Red);
            window.draw(circle);
        }
        window.display();
    }

    return 0;
}
