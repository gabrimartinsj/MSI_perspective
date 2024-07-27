from perspective import Client, Attributes, utils
import pandas as pd
import matplotlib.pyplot as plt

# Função para ler dados usando pandas
def read_text_from_csv(file_path):
    return pd.read_csv(file_path, header=None, names=['text'])

# Configuração da API Perspective
API_KEY = "AIzaSyDv2AtyAj87vvkbwuiFeL-Ju9IAxHE_UE4"
client = Client(token=API_KEY)

# Ler os dados de um arquivo CSV
file_path = "youtube_data_messages.csv"
df = read_text_from_csv(file_path)

# Função para analisar texto usando a API Perspective
def analyze_text(text):
    try:
        response = client.analyze(text=text, attributes=[Attributes.TOXICITY, Attributes.INSULT])
        return response
    except Exception as e:
        print(f"Erro ao processar o texto: {text}\nErro: {e}")
        return {}

# Lista para armazenar os resultados
results = []

print("Iniciando análise dos textos...")
for index, row in df.iterrows():
    text = row['text']
    print(f"Analisando texto: {text}")
    response = analyze_text(text)
    
    if response:
        # Adicionar os resultados à lista
        results.append({
            'text': text,
            'toxicity': response.get("TOXICITY", 0),
            'insult': response.get("INSULT", 0)
        })

print("Análise concluída.")

# Converter os resultados em DataFrame
print("Convertendo resultados em DataFrame...")
df_results = pd.DataFrame(results)

print("Calculando estatísticas...")

# Estatísticas básicas
mean_toxicity = df_results["toxicity"].mean()
mean_insult = df_results["insult"].mean()

# Identificar textos com maior e menor pontuação de toxicidade e insultos
most_toxic_texts = df_results.nlargest(5, 'toxicity')
least_toxic_texts = df_results.nsmallest(5, 'toxicity')
most_insulting_texts = df_results.nlargest(5, 'insult')
least_insulting_texts = df_results.nsmallest(5, 'insult')

# Exibir os resultados agregados
print(f"Média da Toxicidade: {mean_toxicity}")
print(f"Média dos Insultos: {mean_insult}")

# Salvar os textos em um arquivo de texto
with open('top_texts_2.txt', 'w', encoding='utf-8') as file:
    file.write("Textos mais tóxicos:\n")
    for _, row in most_toxic_texts.iterrows():
        file.write(f"Texto: {row['text']} com pontuação {row['toxicity']}\n")
    
    file.write("\nTextos menos tóxicos:\n")
    for _, row in least_toxic_texts.iterrows():
        file.write(f"Texto: {row['text']} com pontuação {row['toxicity']}\n")
    
    file.write("\nTextos mais insultantes:\n")
    for _, row in most_insulting_texts.iterrows():
        file.write(f"Texto: {row['text']} com pontuação {row['insult']}\n")
    
    file.write("\nTextos menos insultantes:\n")
    for _, row in least_insulting_texts.iterrows():
        file.write(f"Texto: {row['text']} com pontuação {row['insult']}\n")

print("Textos principais armazenados em 'top_texts.txt'.")

# Plotar gráficos
plt.figure(figsize=(10, 5))

# Histograma das Toxicidades
plt.subplot(1, 2, 1)
plt.hist(df_results['toxicity'], bins=10, edgecolor='black')
plt.title('Distribuição da Toxicidade')
plt.xlabel('Pontuação de Toxicidade')
plt.ylabel('Frequência')

# Histograma dos Insultos
plt.subplot(1, 2, 2)
plt.hist(df_results['insult'], bins=10, edgecolor='black')
plt.title('Distribuição dos Insultos')
plt.xlabel('Pontuação de Insulto')
plt.ylabel('Frequência')

plt.tight_layout()
plt.show()
