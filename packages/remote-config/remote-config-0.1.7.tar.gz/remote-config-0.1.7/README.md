# Remote Config

Essa biblioteca tem como funcionalidade capturar os mapeamentos de features ativas por clusters e disponibilizar em memória, juntamente com as variáveis de ambientes lá registradas.

## Clusters

O mapeamento dos clusters ficarão listadas dentro da pasta `clusters` que se encontra na pasta `general` na raiz do Key / Value.

Para cada cluster se faz necessário criar uma key com o nome do cluster ex: `cluster-google-merchant`

Contendo a lista de id's das lojas no seguinte formato:

```json
{
  "ids": [123, 456]
}
```

## Feature Toggle

O mapeamento dos clusters ficarão listadas dentro da pasta `feature-toggle` que se encontra na pasta `general` na raiz do Key / Value.

Para cada feature se faz necessário criar uma key com o nome da feature ex: `google-merchant`

O valor dentro desta key deve ser no formato do JSON a baixo:

```json
{
  "enable": true,
  "default": false,
  "clusters": ["general/feature-toggle/cluster-google-merchant"]
}
```

A propriedade `enable` define se a feature está ativada para aplicação como um todo.

A propriedade `cluster` define uma lista dos caminhos dos clusters.

A propriedade `default` define o comportamento padrão caso o `enable` esteja false e a loja não esteja em nenhum cluster.

## Globals

As variaveis que não são atreladas a nenhum cluster específico são denominadas `globals`. Estas se encontram na pasta `globals` (tambem dentro da pasta `general` na raiz do Key / Value).

O valor dentro desta key pode conter qualquer conteúdo que satisfaça um JSON válido.

## Como usar

Inicializando o singleton e já configurando os tempos de atualização de cache

```python
from django.conf import settings
class CoreConfig(AppConfig):
    name = "core"

     def ready(self):
        from remote_config import RemoteConfig
        RemoteConfig(host=URL, port=80, token=TOKEN, feature_minute=5, cluster_minute=5).start()
```

Para fazer uma checagem da feature, basta só iniciar o `RemoteConfig` sem as configurações pois elas já forão inicializadas e chamara a função `get_feature` que retornará um boleano

```python
RemoteConfig().get_feature('google-merchant', 123)
```

Já para para fazer uma checagem da global, basta chamar a função `get_global` que retornará um dicinário com o valor correspondete à chave especificada.

```python
RemoteConfig().get_global('chave-global-qualquer')
```
