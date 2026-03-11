#!/usr/bin/env bash

# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# устанавливаем зависимости, собираем статику, выполняем миграции
make install && make collectstatic && make migrate

