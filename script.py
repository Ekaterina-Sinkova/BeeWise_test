import pandas as pd
pd.options.mode.chained_assignment = None
#!python -m spacy download ru_core_news_md;
import ru_core_news_md;
nlp = ru_core_news_md.load()

test_data = pd.read_csv('test_data.csv')
data_output = test_data.copy(deep=True)
data_output["insight"] = ""
data = test_data[test_data['role'] == 'manager'].reset_index()

class Dialog_parser:
    GREETING = ['здравствуйте', 'приветствую', 'добрый день', 'доброе утро', 'добрый вечер']
    FAREWELL = ['всего хорошего', 'до свидания', 'всего доброго', 'хорошего вам дня', 'хорошего дня','хорошего вечера', 'до встречи', 'до связи', 'будьте здоровы']

    @classmethod
    def has_greeting(cls, str):
        return any([greeting in str.lower() for greeting in cls.GREETING])

    @classmethod
    def has_farewell(cls, str):
        return any([farewell in str.lower() for farewell in cls.FAREWELL])

    @staticmethod
    def get_names(str):
        names = []
        for word in str.split():
            doc =  nlp(word.title())
            for ent in doc.ents:
                if (ent.label_ == 'PER') and (ent.text != 'Алло'):
                    names.append(ent.text)
        return names if names else 0

    def get_greeting(self,data):
        res = pd.DataFrame(columns=['dlg_id', 'line_n', 'text'])
        data['greeting'] = data['text'].apply(self.has_greeting)

        for id in set(data[(data['greeting'] == True)]['dlg_id']):
            text = (data[(data['dlg_id'] == id) & (data['greeting'] == True)]['text']).to_string(index=False)
            line_n = int(data[(data['dlg_id'] == id) & (data['greeting'] == True)]['line_n'])
            res.loc[len(res)] = [id, line_n, text]
            cell = data_output['insight'].loc[(data_output['dlg_id'] == id) & (data_output['line_n'] == line_n)]
            if 'greeting' not in cell.to_string(index=False):
                 data_output['insight'].loc[(data_output['dlg_id'] == id) & (data_output['line_n'] == line_n)] += 'greeting = True '
        return res

    def get_introduction(self,data):
        res = pd.DataFrame(columns=['dlg_id', 'line_n', 'name','text'])
        data['PER'] = data['text'].apply(self.get_names)
        df = data[(data['PER'] != 0) & (data['text'].str.contains(('|').join(['это','зовут', 'говорит', 'представиться'])))]

        for id in set(df['dlg_id']):
            text = df[df['dlg_id'] == id]['text'].iloc[0]
            name = df[df['dlg_id'] == id]['PER'].iloc[0][0].title()
            line_n = df[df['dlg_id'] == id]['line_n'].iloc[0]
            res.loc[len(res)] = [id, line_n, name, text]
            cell = data_output['insight'].loc[(data_output['dlg_id'] == id) & (data_output['line_n'] == line_n)] 
            if 'name' not in cell.to_string(index=False):
                data_output['insight'].loc[(data_output['dlg_id'] == id) & (data_output['line_n'] == line_n)]  += 'name = True '
        return res
    
    def get_company(self, data):
        res = pd.DataFrame(columns=['dlg_id', 'line_n', 'company'])
        df = data[(data['text'].str.contains('компания'))]
        for id in set(df['dlg_id']):
            words = (df[df['dlg_id'] == id]['text'].iloc[0]).split()
            line_n = df[df['dlg_id'] == id]['line_n'].iloc[0]
            company = words[words.index('компания') + 1]
            res.loc[len(res)] = [id, line_n, company]
            cell = data_output['insight'].loc[(data_output['dlg_id'] == id) & (data_output['line_n'] == line_n)]
            if 'company' not in cell.to_string(index=False):
                data_output['insight'].loc[(data_output['dlg_id'] == id) & (data_output['line_n'] == line_n)] += 'company = True '
        return res
    
    def get_farewell(self, data):
        res = pd.DataFrame(columns=['dlg_id', 'line_n', 'text'])
        data['farewell'] = data['text'].apply(self.has_farewell)
        for id in set(data[(data['farewell'] == True)]['dlg_id']):
            text = data[(data['dlg_id'] == id) & (data['farewell'] == True)]['text'].iloc[0]
            line_n = data[(data['dlg_id'] == id) & (data['farewell'] == True)]['line_n'].iloc[0]
            res.loc[len(res)] = [id, line_n, text]
            cell = data_output['insight'].loc[(data_output['dlg_id'] == id) & (data_output['line_n'] == line_n)]
            if 'farewell' not in cell.to_string(index=False):
                data_output['insight'].loc[(data_output['dlg_id'] == id) & (data_output['line_n'] == line_n)] += 'farewell = True '
        return res

    def check_manager(self, data):
        res = pd.DataFrame(columns=['dlg_id', 'Politeness'])

        for id in set(data['dlg_id']):
            hello = id in list(self.get_greeting(data)['dlg_id'])
            goodbye = id in list(self.get_farewell(data)['dlg_id'])
            politeness = hello and goodbye
            res.loc[len(res)] = [id, politeness]
        return res

parser = Dialog_parser()

if __name__ == '__main__':
    while True:
        try:
            task = int(input('''Что делаем?\n
            [1] Извлекаем реплики с приветствием
            [2] Извлекаем реплики, где менеджер представил себя, и имя менеджера 
            [3] Извлекаем название компании
            [4] Извлекаем реплики, где менеджер попрощался
            [5] Проверять требование к менеджеру: «В каждом диалоге обязательно необходимо поздороваться и попрощаться с клиентом»
            [6] Занести отметки в исходный файл
            [0] Закончить работу\n'''))
        except ValueError:
            print('Неправильное значение')

        if task == 1:
            print(parser.get_greeting(data)[['dlg_id', 'text']].to_string(index=False))
            print()
        
        elif task == 2:
            print('Тут надо немного подождать...')
            print(parser.get_introduction(data)[['dlg_id', 'name', 'text']].to_string(index=False))
            print()
        
        elif task == 3:
            print(parser.get_company(data)[['dlg_id', 'company']].to_string(index=False))
            print()
        
        elif task == 4:
            print(parser.get_farewell(data)[['dlg_id', 'text']].to_string(index=False))
            print()

        elif task == 5:
            print(parser.check_manager(data))
            print()

        
        elif task == 6:
            data_output.to_csv('data_output.csv')
            print('Файл data_output.csv сохранен')

        
        elif task == 0:
            break
        
        else:
            print('Неправильное значение')