
from botcity.core import DesktopBot

from botcity.web import WebBot, Browser, By

from botcity.maestro import *

from webdriver_manager.chrome import ChromeDriverManager

BotMaestroSDK.RAISE_NOT_CONNECTED = False

class Veiculo:
    veiculos_cadastrados = []
    quantidade_veiculos = 0
    
    def __init__(self, nome:str, ano:int, diaria:float):
        self.__nome = nome
        self.__ano = ano
        self.__diaria = diaria
        Veiculo.veiculos_cadastrados.append(self)
        Veiculo.calcula_quantidade()
    
    def calcula_aluguel(self, dias):
        aluguel_total = self.__diaria * dias
        if dias > 7:
            desconto = 0.10
            aluguel_total *= (1 - desconto)
        return aluguel_total
    
    @classmethod
    def calcula_quantidade(cls):
        cls.quantidade_veiculos = len(Veiculo.veiculos_cadastrados)
        
    @classmethod
    def aumento_percentual(cls, veiculos:list, porcentagem:float):
        for veiculo in veiculos:
            valor_total = veiculo.diaria * (1 + porcentagem)
            veiculo.diaria = valor_total
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def ano(self):
        return self.__ano
    
    @property
    def diaria(self):
        return self.__diaria
    
    @nome.setter
    def nome(self, novo_nome:str):
        if type(novo_nome) != str:
            print('Nome inválido.')
        else:
            self.__nome = novo_nome
     
    @ano.setter       
    def ano(self, novo_ano:int):
        if novo_ano < 0:
            print('Ano inválido.')
        else:
            self.__ano = novo_ano
            
    @diaria.setter
    def diaria(self, nova_diaria:float):
        if nova_diaria < 0:
            print('Valor inválido.')
        else:
            self.__diaria = nova_diaria
            
    

class Carro(Veiculo):
    def __init__(self, nome:str, ano:int, diaria:float, combustivel:str):
        Veiculo.__init__(self, nome, ano, diaria)
        self.combustivel = combustivel
        
    def calcula_aluguel(self, dias:int, cupom = 0):
        aluguel_total = super().calcula_aluguel(dias)
        aluguel_total -= cupom
        return aluguel_total
    
        
    
    
class Motocicleta(Veiculo):
    def __init__(self, nome:str, ano:int, diaria:float, combustivel:str, cilindrada:int):
        Veiculo.__init__(self, nome, ano, diaria)
        self.combustivel = combustivel
        self.cilindrada = cilindrada
        
    def calcula_aluguel(self, dias:int, cupom = 0):
        aluguel_total = super().calcula_aluguel(dias)
        taxa = 0
        if self.cilindrada > 200:
            taxa = 0.10
        aluguel_total *= (1 + taxa)
        aluguel_total -= cupom
        return aluguel_total
 
    
def cadastrar_veiculo(desktopbot:DesktopBot, webbot:WebBot, veiculo):        
    if not desktopbot.find("Type", matching=0.97, waiting_time=10000):
        not_found("Type")
    desktopbot.click_relative(46, 51)
    if isinstance(veiculo, Carro):
        if not desktopbot.find("Carro", matching=0.97, waiting_time=10000):
            not_found("Carro")
        desktopbot.click_relative(33, 47)
    else:
        if not desktopbot.find("Motocicleta", matching=0.97, waiting_time=10000):
            not_found("Motocicleta")
        desktopbot.click_relative(29, 72)
        
    while len(webbot.find_elements('//*[@id="nomeVeiculo"]', By.XPATH)) < 1:
        webbot.wait(1000)
        print("Carregando...")
    webbot.find_element('//*[@id="nomeVeiculo"]', By.XPATH).click()
    webbot.kb_type(veiculo.nome)
    
    while len(webbot.find_elements('//*[@id="anoVeiculo"]', By.XPATH)) < 1:
        webbot.wait(1000)
        print("Carregando...")
    webbot.find_element('//*[@id="anoVeiculo"]', By.XPATH).click()
    webbot.kb_type(str(veiculo.ano))
    
    while len(webbot.find_elements('//*[@id="custoDiaria"]', By.XPATH)) < 1:
        webbot.wait(1000)
        print("Carregando...")
    webbot.find_element('//*[@id="custoDiaria"]', By.XPATH).click()
    webbot.kb_type(str(veiculo.diaria))
    
    if veiculo.combustivel.lower() == "etanol":
        if not desktopbot.find("tipo_combus", matching=0.97, waiting_time=10000):
            not_found("tipo_combus")
        desktopbot.click_relative(11, 42)
    elif veiculo.combustivel.lower() == "gasolina":
        if not desktopbot.find("tipo_combus1", matching=0.97, waiting_time=10000):
            not_found("tipo_combus1")
        desktopbot.click_relative(-27, 72)
    else:
        if not desktopbot.find("tipo_combus2", matching=0.97, waiting_time=10000):
            not_found("tipo_combus2")
        desktopbot.click_relative(12, 94)
        
    if isinstance(veiculo, Motocicleta):
        webbot.find_element('//*[@id="cilindrada"]', By.XPATH).click()
        webbot.kb_type(str(veiculo.cilindrada))
        
    webbot.find_element('/html/body/div/form/div[7]/button', By.XPATH).click()
    
    webbot.wait(3000)
    
    if not desktopbot.find("retornar", matching=0.97, waiting_time=10000):
        not_found("retornar")
    desktopbot.click()
    webbot.wait(1000)      
    dados_veiculos(veiculo)
    
    
    
    
def cadastrar_aluguel(webbot:WebBot, veiculo, dias, cupom = 0):
    aluguel = veiculo.calcula_aluguel(dias)
    webbot.wait(1000)
    while len(webbot.find_elements('/html/body/div/form/div[7]/a', By.XPATH)) < 1:
        webbot.wait(1000)
        print("Carregando...")
    webbot.find_element('/html/body/div/form/div[7]/a', By.XPATH).click()
    
    while len(webbot.find_elements('/html/body/div/div/a[2]', By.XPATH)) < 1:
        webbot.wait(1000)
        print("Carregando...")
    webbot.find_element('/html/body/div/div/a[2]', By.XPATH).click()
    
    while len(webbot.find_elements('//*[@id="nomeVeiculo"]', By.XPATH)) < 1:
        webbot.wait(1000)
        print("Carregando...")
    webbot.find_element('//*[@id="nomeVeiculo"]', By.XPATH).click()
    webbot.kb_type(veiculo.nome)
    
    webbot.find_element('//*[@id="dias"]', By.XPATH).click()
    webbot.kb_type(str(dias))
    
    webbot.find_element('//*[@id="valorTotal"]', By.XPATH).click()
    webbot.kb_type(str(aluguel))
    
    webbot.find_element('//*[@id="formAluguel"]/div[4]/button', By.XPATH).click()
    
    webbot.wait(3000)
    
    while len(webbot.find_elements('/html/body/div/div/a[2]', By.XPATH)) < 1:
        webbot.wait(1000)
        print("Carregando...")
    webbot.find_element('/html/body/div/div/a[2]', By.XPATH).click()
    
    while len(webbot.find_elements('/html/body/div/div/a[1]', By.XPATH)) < 1:
        webbot.wait(1000)
        print("Carregando...")
    webbot.find_element('/html/body/div/div/a[1]', By.XPATH).click()
    webbot.wait(1000)
    
    dados_alugueis(veiculo, dias, aluguel)
    
    
    
def dados_veiculos(veiculo):
    with open("dados_veiculos.txt", "a") as arquivo:
        arquivo.write(f"Nome: {veiculo.nome}\nAno: {veiculo.ano}\nDiária: {veiculo.diaria}\nCombustível: {veiculo.combustivel}\n")
        if isinstance(veiculo, Motocicleta):
            arquivo.write(f"Cilindradas: {veiculo.cilindrada}\n\n")
        else:
            arquivo.write("\n")
    
def dados_alugueis(veiculo, dias, aluguel):
    with open("dados_alugueis.txt", "a") as arquivo:
        arquivo.write(f"Nome: {veiculo.nome}\nAlugado por {dias} dias\nValor do aluguel: R${aluguel:.2f}\n\n")
        

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")   
    print(f"Task Parameters are: {execution.parameters}")

    desktopbot = DesktopBot()

    webbot = WebBot()

    webbot.headless = False

    webbot.browser = Browser.CHROME

    webbot.driver_path = ChromeDriverManager().install()

    webbot.browse("http://127.0.0.1:5500/templates/formulario.html")
    webbot.maximize_window()

    # Implement here your logic...
    motocicleta1 = Motocicleta("Kawasaki Ninja", 2012, 75, "Álcool", 300)
    motocicleta2 = Motocicleta("Biz 125", 2023, 45, "Gasolina", 125)
    carro1 = Carro("Fiat Palio", 2017, 70, "Gasolina")
    carro2 = Carro("Renault Kwid", 2020, 75, "Gasolina")
    
    try:
        cadastrar_veiculo(desktopbot, webbot, motocicleta1)
        cadastrar_veiculo(desktopbot, webbot, carro1)
        
        cadastrar_aluguel(webbot, carro1, 5)
    except Exception as ex:
        print(f"Erro: {ex}")

    # Wait 3 seconds before closing
    webbot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    webbot.stop_browser()

def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
