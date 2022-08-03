import requests
from bs4 import BeautifulSoup

languages = ['Arabic',
             'German',
             'English',
             'Spanish',
             'French',
             'Hebrew',
             'Japanese',
             'Dutch',
             'Polish',
             'Portuguese',
             'Romanian',
             'Russian',
             'Turkish']

print('Hello, welcome to the translator. Translator supports:')
for i, language in enumerate(languages, 1):
    print(f'{i}. {language}')

print('Type the number of your language:')
source_lang = languages[int(input())-1]
print('Type the number of language you want to translate to:')
target_lang = languages[int(input())-1]

translation_dir = f'{source_lang}-{target_lang}'.lower()

print('Type the word you want to translate:')
word = input()



headers = {'User-Agent': 'Mozilla/5.0'}
while True:
    r = requests.get(f'https://context.reverso.net/translation/{translation_dir}/{word}', headers=headers)
    if r.status_code == 200:
        # print(f'{r.status_code} OK')
        break

soup = BeautifulSoup(r.content, 'html.parser')

print(f'\n{target_lang.capitalize()} Translations:')

# Translations
translations = []
for translation in soup.find_all('a', {'class': 'translation'}):
    # print(translation)
    translations.append(translation.get('data-term'))
    print(translations[-1])

# Sentences
print(f'\n{target_lang.capitalize()} Examples:')
examples = []
for example in soup.find_all('div', {'class': 'src ltr'}):
    if not example.parent.get('class') is None:
        if example.parent.get('class')[0] == 'example':
            examples.append([example.text.strip(), ''])

i = 0
for example_trg in soup.find_all('div', {'class': 'trg ltr'}):
    if not example_trg.parent.get('class') is None:
        if example_trg.parent.get('class')[0] == 'example':
            examples[i][1] = example_trg.text.strip()

            print(f'{examples[i][1]}:')
            print(examples[i][0])
            print()
            i = i + 1

