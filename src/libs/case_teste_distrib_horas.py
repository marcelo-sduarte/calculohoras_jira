import unittest

def distribuir_horas(horas, partes):
    if partes < 1:
        raise Exception(f"Numero negativo em partes: {partes}")
      
    # Inicializa a lista com partes iguais a 8
    distribuicao = [8] * partes

    # Verifica se há somente uma parte
    if partes == 1 or horas <= 8 :
        distribuicao = []
        distribuicao.append(horas)
        return distribuicao,partes
    elif partes == 2:
        distribuicao = []
        horas_distribuidas = horas / partes
        for i in range(partes):
            distribuicao.append(horas_distribuidas)
    
    # Calcula a soma inicial das partes
    soma_total = sum(distribuicao)

    # Define os múltiplos de 8 a serem adicionados em ordem crescente
    multiplos_de_8 = [8 * i for i in range(1, 26)]

    # Verifica se a soma total é menor que o número de horas desejado
    if soma_total < horas:
        # Adiciona partes extras, respeitando o total de partes e o número de horas desejado
        for multiplo in multiplos_de_8:
            if soma_total == horas:
                    break
            for index,num in enumerate(distribuicao):
                if soma_total == horas:
                    break
                if soma_total < horas:
                    distribuicao.pop(index)
                    distribuicao.append(multiplo)
                    soma_total = sum(distribuicao)
                else:
                    distribuicao.pop()
                    distribuicao.append(8)
                    soma_total = sum(distribuicao)
    elif soma_total > horas:
        diferenca_horas = soma_total - horas
        dif_qtd = (diferenca_horas /8)+1
        for i in range(int(dif_qtd)):
            if soma_total == horas:
                break
            distribuicao.pop(i)
            soma_total = sum(distribuicao)
            partes_total = len(distribuicao)
        if soma_total < horas:
            diferenca_horas = horas - soma_total
            distribuicao.append(diferenca_horas)
            soma_total = sum(distribuicao)

    # ajuste tamanho se necessário
    if len(distribuicao) != partes:
        saldo_partes = partes - partes_total
        for saldo in range(saldo_partes):
            distribuicao.append(1)
            soma_total = sum(distribuicao)
    # Ajusta hora se necessário
    if soma_total != horas:
        diferenca_horas = horas  - soma_total
        if diferenca_horas < 0 :
            for index, numero in enumerate(distribuicao):
                diferenca_horas = horas  - soma_total
                if soma_total == horas:
                    break
                value = distribuicao[index]
                if value > abs(diferenca_horas):
                    saldo_horas = value - abs(diferenca_horas)
                    distribuicao[index] = saldo_horas
                    soma_total = sum(distribuicao)
        #diferenca = horas - soma_total
        #distribuicao[-1] += diferenca
    if horas == soma_total and partes == len(distribuicao):
        print(f"TESTE COM SUCESSO EM  horas: {horas} partes: {partes}")
    else:
        print(f"TESTE COM FALHA EM  horas: {horas} partes: {partes}")
    return distribuicao,partes


class TestDistribuirHoras(unittest.TestCase):

    def test_distribuicao_horas(self):
    # Lista de combinações de horas e partes
        # Lista de tuplas para a primeira sequência de testes (176, X)
        sequencia_176 = [(176, partes) for partes in range(14, 0, -1)]

        # Lista de tuplas para a segunda sequência de testes (168, X) até (8, X)
        sequencia_168_8 = [(horas, partes) for horas in range(168, 0, -8) for partes in range(14, 0, -1)]

        # Combina as duas sequências usando zip()
        combinacoes = sequencia_176 + sequencia_168_8
        # Loop sobre as combinações e execução do teste para cada uma
        for horas, partes in combinacoes:
            with self.subTest(horas=horas, partes=partes):
                resultado, partes = distribuir_horas(horas, partes)
                self.assertEqual(sum(resultado), horas)  # Verifica a soma das horas distribuídas
                self.assertEqual(partes, partes)  # Verifica o número de partes


if __name__ == '__main__':
    unittest.main()


#resultado,partes = distribuir_horas(176, 12)
#print("Resultado final:", resultado)
#print(f"partes:{partes}" )
#print(f"len distr:{len(resultado)}" )

#print(f"sum distr:{sum(resultado)}" )


## VERSAO MAIS ESTAVEL EM TESTES DE 80 HORAS DIVIDIDAS  EM PARTES DE 1 A 12








   # Lista de múltiplos de 8 em ordem crescente
   # multiplos_de_8 = [8 * i for i in range(1, 26)]
   #multiplos_de_8 = [1, 2, 3, 4, 5, 6, 7, 8, 16, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200]