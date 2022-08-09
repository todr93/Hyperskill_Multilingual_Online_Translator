import requests
from bs4 import BeautifulSoup
import argparse

class NoLanguageError(Exception):
    def __init__(self, language):
        self.message = f"Sorry, the program doesn't support {language}"
        super().__init__(self.message)


languages = ['all',
             'arabic',
             'german',
             'english',
             'spanish',
             'french',
             'hebrew',
             'japanese',
             'dutch',
             'polish',
             'portuguese',
             'romanian',
             'russian',
             'turkish']

# Argumenty CLI
parser = argparse.ArgumentParser(description="Program is used for translations")
# parser.add_argument("source_lang", choices=languages, help="Choose one language of the list")
# parser.add_argument("target_lang", choices=languages, help="Choose one language of the list")
parser.add_argument("source_lang")
parser.add_argument("target_lang")
parser.add_argument("word")

args = parser.parse_args()

ok = True

source_lang = args.source_lang
if source_lang not in languages:
    print(f"Sorry, the program doesn't support {source_lang}")
    ok = False

target_lang = args.target_lang
if target_lang not in languages:
    print(f"Sorry, the program doesn't support {target_lang}")
    ok = False

if target_lang == 'all':
    target_langs = languages[1:]
else:
    target_langs = [target_lang]

# print('Type the word you want to translate:')
# word = input()
word = args.word

# Utworzenie pliku
if ok == True:
    with open(f'{word}.txt', 'w', encoding='utf-8') as file:

        for target_lang in target_langs:
            if target_lang == source_lang:
                continue

            translation_dir = f'{source_lang}-{target_lang}'.lower()

            headers = {'User-Agent': 'Mozilla/5.0'}
            while True:
                try:
                    r = requests.get(f'https://context.reverso.net/translation/{translation_dir}/{word}', headers=headers)
                    # print(f'https://context.reverso.net/translation/{translation_dir}/{word}')
                except Exception:
                    print("Something wrong with your internet connection")
                if r.status_code == 200:
                    # print(f'{r.status_code} OK')
                    break
                else:
                    # print("Something wrong with your internet connection")
                    break
            # if r.status_code != 200:
            #     break

            soup = BeautifulSoup(r.content, 'html.parser')

            # Sprawdzenie czy znaleziono tlumaczenie
            if 'not found' in soup.find('section', {'id': 'no-results'}).getText():
                print(f"Sorry, unable to find {word}")
                break

            print(f'\n{target_lang.capitalize()} Translations:')
            file.write(f'\n{target_lang.capitalize()} Translations:\n')

            # Translations
            translations = []
            for translation in soup.find_all('a', {'class': 'translation'}):
                # print(translation)
                if not translation.get('data-term') is None:
                    translations.append(translation.get('data-term'))
                    print(translations[-1])
                    file.write(f'{translations[-1]}\n')

            # Sentences
            print(f'\n{target_lang.capitalize()} Examples:')
            file.write(f'\n{target_lang.capitalize()} Examples:\n')
            examples = []
            for example in soup.find_all('div', {'class': 'src'}):
                if not example.parent.get('class') is None:
                    if example.parent.get('class')[0] == 'example':
                        examples.append([example.text.strip(), ''])

            i = 0
            for example_trg in soup.find_all('div', {'class': 'trg'}):
                if not example_trg.parent.get('class') is None:
                    if example_trg.parent.get('class')[0] == 'example':
                        examples[i][1] = example_trg.text.strip()

                        if i == 0:
                            print(f'{examples[i][1]}:')
                            file.write(f'{examples[i][1]}:\n')
                            print(examples[i][0])
                            file.write(f'{examples[i][0]}\n\n')
                            print()
                        i = i + 1
