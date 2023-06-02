from csv import writer

def to_csv(List_of_data): #функция экспорта 
    with open('pneumatic_armature_parser_table.csv', 'a', encoding="utf-8") as f_object: #открываем файл с кодировкой utf
        writer_object = writer(f_object, delimiter=",", lineterminator='\n') #
        writer_object.writerow(List_of_data) #размещаем переданный лист 
        f_object.close() #закрываем поток
