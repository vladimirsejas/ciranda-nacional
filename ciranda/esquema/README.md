# Esquema do serviço Ciranda

`servico.schema.json` descreve a forma completa emitida pelo conversor atual: os 12 campos de `CAMPOS_PERMITIDOS`, tipos e limite textual. O esquema não adiciona dependências nem é executado automaticamente pelo importador.

A conformidade compara a lista de propriedades do esquema com `CAMPOS_PERMITIDOS`. A validação efetiva dos documentos recebidos continua sendo feita pelo código Python de importação e conformidade.
