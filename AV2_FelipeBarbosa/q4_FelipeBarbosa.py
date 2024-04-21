# Elabore um Scaffold que facilite a vida do programador ao escrever
# qualquer consulta SQL que envolva as tabelas da questão anterior.
# O Scaffold deverá ter?
# (I) uma função em Python que implementa a geração do código do INNER JOIN entre as tabelas GAMES, VIDEOGAMES e COMPANY
# (II) outra para gerar o comando SELECT nos atributos envolvidos.


USERS = lambda : ("Users", {"id": "int", "name": "varchar (100)", "country": "varchar (100)", "id_console": "int"})
GAMES = lambda : ("Games", {"id_game": "int", "title": "varchar (100)", "genre": "varchar (100)", "release_date": "date", "id_console": "int"})
VIDEOGAMES = lambda : ("Videogames", {"id_console": "int", "name": "varchar (100)", "id_company": "int", "release_date": "date"})
COMPANY = lambda : ("Company", {"id_company": "int", "name": "varchar (100)", "country": "varchar (100)"})

handle_parameter = lambda table_char, parameter: "{}.{}".format(table_char, parameter)
get_field_with_alias = lambda table_name, parameter : handle_parameter(get_table_char(table_name), parameter)
get_fields_with_alias = lambda table, indexes: ", ".join([handle_parameter(get_table_char(table[0]), get_table_key(table, index)) for index in indexes])
handle_inner_join_on  = lambda parameter, table_left_name, table_right_name : "{} = {}".format(get_field_with_alias(table_left_name, parameter), get_field_with_alias(table_right_name, parameter))
set_table_char = lambda table_name : "{} {}".format(table_name, table_name[0].lower())
get_table_char = lambda table_name : table_name[0].lower()
get_table_keys_as_list = lambda table : list(table[1].keys())
get_table_key = lambda table, index : get_table_keys_as_list(table)[index]

# (I) 
gen_inner_join = lambda join_parameter, table_left, table_right, first_join : "INNER JOIN {} ON {}".format(set_table_char(table_right[0]), handle_inner_join_on(join_parameter, table_left[0], table_right[0])) if not first_join else "{} INNER JOIN {} ON {}".format(set_table_char(table_left[0]), set_table_char(table_right[0]), handle_inner_join_on(join_parameter, table_left[0], table_right[0]))
# (II)
mount_select_label = lambda fields = None : "SELECT {} FROM".format("({})".format(", ".join(fields)) if fields else "*")
gen_select = lambda select, inner_join_labels : select if not inner_join_labels else gen_select("{} {}".format(select, inner_join_labels[0]), inner_join_labels[1:])


print(gen_select(
    mount_select_label([get_fields_with_alias(VIDEOGAMES(), [1, 2]), get_fields_with_alias(GAMES(), [0, 1])]),
    [gen_inner_join(get_table_key(GAMES(), 4), GAMES(), VIDEOGAMES(), True),
    gen_inner_join(get_table_key(VIDEOGAMES(), 2), VIDEOGAMES(), COMPANY(), False)]
) + ";")