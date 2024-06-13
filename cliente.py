import requests

# URL base da API
base_url = 'http://3.229.255.117'

# Função para adicionar uma viagem
def add_trip():
    destination = input("Digite a cidade de destino: ")
    start_date = input("Digite a data de início da viagem (dd/mm/aaaa): ")
    end_date = input("Digite a data de término da viagem (dd/mm/aaaa): ")
    url = f'{base_url}/add_trip'
    data = {
        'destination': destination,
        'start_date': start_date,
        'end_date': end_date
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        trip_id = response.json()['id']
        print(f'Viagem adicionada com sucesso! ID: {trip_id}')
    else:
        print('Erro ao adicionar viagem.')

# Função para modificar uma viagem
def update_trip():
    trip_id = input("Digite o ID da viagem a ser modificada: ")
    destination = input("Digite a nova cidade de destino: ")
    start_date = input("Digite a nova data de início da viagem (dd/mm/aaaa): ")
    end_date = input("Digite a nova data de término da viagem (dd/mm/aaaa): ")
    url = f'{base_url}/trips/{trip_id}'
    data = {
        'destination': destination,
        'start_date': start_date,
        'end_date': end_date
    }
    response = requests.put(url, json=data)
    if response.status_code == 204:
        print('Viagem modificada com sucesso.')
    else:
        print('Erro ao modificar viagem.')

# Função para remover uma viagem
def delete_trip():
    trip_id = input("Digite o ID da viagem a ser removida: ")
    url = f'{base_url}/trips/{trip_id}'
    response = requests.delete(url)
    if response.status_code == 204:
        print('Viagem removida com sucesso.')
    else:
        print('Erro ao remover viagem.')

# Menu principal
while True:
    print("\nMenu:")
    print("1. Adicionar viagem")
    print("2. Modificar viagem")
    print("3. Remover viagem")
    print("4. Finalizar")

    choice = input("Escolha uma opção: ")

    if choice == '1':
        add_trip()
    elif choice == '2':
        update_trip()
    elif choice == '3':
        delete_trip()
    elif choice == '4':
        print("Programa finalizado.")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
