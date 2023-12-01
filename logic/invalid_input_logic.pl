% Estado inicial do jogo
estado_jogo(inicial).

% Definição de movimentos válidos
movimento_valido(inicial, 'd7c7').

% Verificar se um movimento é válido
movimento_valido(Movimento) :-
    estado_jogo(Estado),
    movimento_valido(Estado, Movimento).

% Lógica para verificar se a entrada é válida
entrada_valida(Movimento) :-
    movimento_valido(Movimento),
    format('Movimento ~w é válido.~n', [Movimento]).
entrada_valida(Movimento) :-
    \+ movimento_valido(Movimento),
    format('Movimento ~w é inválido.~n', [Movimento]).

% Exemplos de consulta
:- entrada_valida('d7c7'). % Movimento válido
:- entrada_valida('x4d3'). % Movimento inválido
