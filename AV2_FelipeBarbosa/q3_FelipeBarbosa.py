# Desenvolva um programa em Python que possui: 
# (I) uma tabela USERS formada pelos atributos id, name, country, id_console
# (II) uma tabela VIDEOGAMES, formada pelos atributos id_console, name, id_company e release_date
# (III) GAMES, formada pelos atributos id_game, title, genre, release_date e id_console;
# (IV) uma tabela COMPANY, com os atributos id_company, name, country.
# (V) Integração com o Banco de Dados MySQL e permitir inserção, remoção e consulta a qualquer registro de qualquer uma das tabelas

import mysql.connector
# (I)
USERS = lambda : ("Users", {"id": "int", "name": "varchar (100)", "country": "varchar (100)", "id_console": "int"})
# (II)
VIDEOGAMES = lambda : ("Videogames", {"id_console": "int", "name": "varchar (100)", "id_company": "int", "release_date": "date"})
# (III)
GAMES = lambda : ("Games", {"id_game": "int", "title": "varchar (100)", "genre": "varchar (100)", "release_date": "date", "id_console": "int"})
# (IV)
COMPANY = lambda : ("Company", {"id_company": "int", "name": "varchar (100)", "country": "varchar (100)"})

create_parameter = lambda name, type : "{} {},".format(name, type)
type_handling = lambda data : [type(x).__name__ if type(x).__name__ != "str" else "varchar (100)" for x in list(data)]
handle_parameter = lambda table_char, parameter: "{}.{}".format(table_char, parameter)
handle_inner_join_on  = lambda parameter, table_left_name, table_right_name : "{} = {}".format(handle_parameter(get_table_char(table_left_name), parameter), handle_parameter(get_table_char(table_right_name), parameter))
set_table_char = lambda table_name : "{} {}".format(table_name, table_name[0].lower())
get_table_char = lambda table_name : table_name[0].lower()
get_table_keys_as_list = lambda table : list(table[1].keys())
get_table_key = lambda table, index : get_table_keys_as_list(table)[index]

# (V)
gen_create_table = lambda table_name, parameter_dict : """
    CREATE TABLE {} (
        {}
    );
""".format(table_name, '\n\t'.join([create_parameter(x, parameter_dict[x]) for x in parameter_dict.keys()]))
gen_insert_table = lambda table, data : "INSERT INTO {} ({}) VALUES ({});".format(table[0], ", ".join(list(data.keys())), ", ".join([data[x] if str(data[x]).isnumeric() else '"{}"'.format(data[x]) for x in list(data.keys())]))
gen_select = lambda table, fields = None : "SELECT {} FROM {};".format("({})".format(", ".join(fields)) if fields else "*", table[0])
gen_delete_where = lambda table, condition : "DELETE FROM {} WHERE {};".format(table[0], condition)

#Criação
print(gen_create_table("Users", {"id": "int", "name": "varchar (100)", "country": "varchar (100)", "id_console": "int"}))
# Consulta
print(gen_select(USERS()))
print(gen_select(USERS(),
                 [get_table_key(USERS(), 1),
                 get_table_key(USERS(), 2)]
        ))
# Inserção
print(gen_insert_table(USERS(), {"name": "Felipe", "age": "20", "gender": "male", "country": "Brazil"}))
# Remoção
print(gen_delete_where(COMPANY(), "id_company = 8"))
# Conexão com BD
db_user = ""
db_password = ""
host = ""
database = ""
cnx = mysql.connector.connect(user=db_user, password=db_password, host=host, database=database)
exec_command = lambda query: cnx.cursor().execute(query)
exec_command(gen_select(USERS()))