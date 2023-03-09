Como o nosso servidor pertence à rede UA temos de nos conectar através de uma VPN. Para isso usamos a aplicação "Check point".

Para conectar à VPN da UA:

    site:
    - go.ua.pt

    Username e password:
    - são as credencias da conta da UA

Para ligar o Django(dentro da pasta /app):
- python manage.py runserver

Para ligar,desligar e reiniciar o Grafana no Windows:
- Aceder ao gestor de tarefas 
- Procurar na aba serviços pelo serviço "Grafana"
- Clicar com o lado direito do rato no serviço e escolher a opção

Para ligar,desligar e reiniciar o Grafana no Linux:
- sudo systemctl start grafana-server.service
- sudo systemctl stop grafana-server.service
- sudo systemctl restart grafana-server.service