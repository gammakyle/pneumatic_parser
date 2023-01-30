from csv import writer

def to_csv(List_of_data):
    with open('pneumatic_armature_parser_table.csv', 'a', encoding="utf-8") as f_object:
        writer_object = writer(f_object, delimiter=";", lineterminator='\n')
        writer_object.writerow(List_of_data)
        f_object.close()
