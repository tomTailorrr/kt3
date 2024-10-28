import pandas as pd
import matplotlib.pyplot as plt
import os

def read_yob_file(filename):
    df = pd.read_csv(filename, names=['Name', 'Sex', 'Count'])
    df['Year'] = int(filename.split('.')[0][-4:])  # Добавляем столбец с годом
    return df

def combine_yob_files(directory):
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    df_list = [read_yob_file(f) for f in all_files]
    combined_df = pd.concat(df_list, ignore_index=True)  # Объединяем все DataFrame в один
    return combined_df

def validate_year_input(year_input):
    try:
        year = int(year_input)
        if year < 1880 or year > 2010:
            raise ValueError(f"Ошибка: год {year} вне диапазона (1880-2010). Пожалуйста, введите корректный год.")
        return year
    except ValueError:
        raise ValueError(f"Ошибка: '{year_input}' не является корректным годом. Пожалуйста, введите числовое значение.")

def plot_charts(df, year):
    data_for_year = df[df['Year'] == year]

    # Круговая диаграмма: распределение по полу
    sex_counts = data_for_year.groupby('Sex')['Count'].sum()
    plt.subplot(1, 2, 1)
    plt.pie(sex_counts, labels=sex_counts.index, autopct=lambda p: f'{int(p * sum(sex_counts) / 100)}', colors=['lightblue', 'lightpink'])
    plt.title(f"Распределение по полу в {year} году")

    # Круговая диаграмма: самые популярные имена
    top_names = data_for_year.groupby('Name')['Count'].sum().nlargest(10)
    plt.subplot(1, 2, 2)
    plt.pie(top_names, labels=top_names.index, autopct='%1.1f%%')
    plt.title(f"Самые популярные имена в {year} году")

    plt.tight_layout()
    plt.show()

def plot_names(df, names):
    # Фильтруем данные по именам
    filtered_df = df[df['Name'].isin(names)]
    
    # Группируем данные по годам и именам
    total_counts = filtered_df.groupby('Name')['Count'].sum()

    # Круговая диаграмма: общее количество
    plt.pie(total_counts, labels=total_counts.index, autopct=lambda p: f'{int(p * sum(total_counts) / 100)}', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.title("Общее количество младенцев с именами")

    plt.tight_layout()
    plt.show()

def plot_trend(df, names):
    # Фильтруем данные по именам
    filtered_df = df[df['Name'].isin(names)]
    
    # Группируем данные по годам
    years_range = pd.Series(range(1880, 2011))
    counts_per_name_year = filtered_df.groupby(['Year', 'Name'])['Count'].sum().unstack(fill_value=0)
    counts_per_name_year = counts_per_name_year.reindex(years_range, fill_value=0)
    
    plt.figure(figsize=(18, 6))

    # Абсолютные значения (количество младенцев с именами по годам)
    plt.subplot(1, 2, 1)
    for name in names:
        plt.plot(counts_per_name_year.index, counts_per_name_year[name], label=name)
    plt.title("Количество младенцев с указанными именами")
    plt.xlabel('Год')
    plt.ylabel('Количество')
    plt.legend()

    # Линия общего количества младенцев с выбранными именами по годам
    plt.subplot(1, 2, 2)
    total_name_counts = counts_per_name_year.sum(axis=1)
    plt.plot(total_name_counts.index, total_name_counts, label="Общее количество", color="purple")
    plt.title("Общее количество младенцев с выбранными именами (1880-2010)")
    plt.xlabel('Год')
    plt.ylabel('Общее количество')
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_selected_names_trend(df, names):
    # Фильтруем данные по именам
    filtered_df = df[df['Name'].isin(names)]

    # Группируем данные по годам
    years_range = pd.Series(range(1880, 2011))
    counts_per_name_year = filtered_df.groupby(['Year', 'Name'])['Count'].sum().unstack(fill_value=0)
    counts_per_name_year = counts_per_name_year.reindex(years_range, fill_value=0)

    plt.figure(figsize=(10, 6))
    plt.title("Динамика имен с 1880 по 2010 год")
    plt.xlabel('Год')
    plt.ylabel('Количество')
    plt.grid()
    for name in names:
        plt.plot(counts_per_name_year.index, counts_per_name_year[name], label=name)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_top_names(df, top_n=10):
    # Группируем данные по именам и суммируем количество младенцев
    name_counts = df.groupby('Name')['Count'].sum().sort_values(ascending=False)
    
    # Отбираем топ-N имен
    top_names = name_counts.head(top_n)
    
    # Визуализация
    plt.figure(figsize=(10, 6))
    plt.barh(top_names.index, top_names.values, color='skyblue')
    plt.gca().invert_yaxis()  # Разворачиваем график для удобства
    plt.title(f"Топ-{top_n} самых популярных имен (1880-2010)")
    plt.xlabel("Количество младенцев")
    plt.ylabel("Имя")
    plt.tight_layout()
    plt.show()

# Загрузка данных
directory = 'yob'
df = combine_yob_files(directory)

# Ввод года пользователем
while True:
    print('Введите год (1880-2010):')
    year_input = input()

    try:
        year_to_plot = validate_year_input(year_input)
        break  # Если год введен корректно, выходим из цикла
    except ValueError as e:
        print(e)  # Выводим сообщение об ошибке и продолжаем цикл

# Построение первых двух графиков
plot_charts(df, year_to_plot)

# Список имен для анализа
names_to_plot = ['Johnny', 'Natalie', 'Bob']  
# Построение кругового графика для указанных имен
plot_names(df, names_to_plot)

# Построение линейного графика для динамики имен с 1880 по 2010
plot_trend(df, names_to_plot)

# Построение отдельного линейного графика для выбранных имен
plot_selected_names_trend(df, names_to_plot)

# Построение графика с самыми популярными именами
plot_top_names(df)
