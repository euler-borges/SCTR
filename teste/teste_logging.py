import logging

# Configurar o logging para escrever no arquivo "meu_log.log"
logging.basicConfig(
    filename='log.log',
    level=logging.DEBUG,              # Define o nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato da mensagem
)

# Exemplos de logs
logging.debug('Isso e um log de DEBUG')
logging.info('Isso e um log de INFO')
logging.warning('Isso e um log de WARNING')
logging.error('Isso e um log de ERROR')
logging.critical('Isso e um log de CRITICAL')
