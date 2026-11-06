# OpenTimer

Aplicativo leve para cronômetro e rotinas de temporizador configuráveis.

## Requisitos

- Python 3.10 ou superior
- CustomTkinter

Instale a dependência:

```bash
python -m pip install customtkinter
```

## Executar

Na raiz do projeto:

```bash
python -m src.window.App
```

## Funcionalidades

- Inicie e pare o cronômetro na tela inicial minimalista.
- Crie modelos com etapas nomeadas, duração em minutos e número de ciclos,
  como uma rotina Pomodoro.
- Inicie um modelo salvo com um clique; a tela inicial mostra a etapa e o tempo restante.
- Alterne entre os temas claro e escuro no menu Aparência.
- Modelos e tema são salvos em `~/.opentimer/settings.json`.

Modelos criados em versões anteriores, com uma única duração, são carregados
como uma etapa e um ciclo.
